<template>
  <nav class="navbar navbar-dark bg-dark px-3 mb-3">

  <span class="navbar-brand">
    Manage Staff
  </span>

  <div>

    <button class="btn btn-outline-light me-2" @click="goDashboard">
      Dashboard
    </button>

    <button class="btn btn-outline-light me-2" @click="goUsers">
      Users
    </button>

    <button class="btn btn-outline-light me-2" @click="goStaff">
      Staff
    </button>

    <button class="btn btn-outline-light me-2" @click="goTreks">
      Treks
    </button>

    <button class="btn btn-outline-light me-2" @click="goBookings">
      Bookings
    </button>

    <button class="btn btn-danger" @click="logout">
      Logout
    </button>

  </div>

</nav>
  <div class="container mt-4">

    <h2 class="mb-4">
      Manage Staff
    </h2>

    <div class="row mb-3">

  <div class="col-md-10">

    <input
      type="text"
      class="form-control"
      placeholder="Search staff by username..."
      v-model="searchKeyword"
    >

  </div>

  <div class="col-md-2">

    <button
      class="btn btn-primary w-100"
      @click="searchStaff"
    >
      Search
    </button>

  </div>

</div>

    <table class="table table-bordered table-striped">

      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="staff in staffs" :key="staff.id">

          <td>{{ staff.id }}</td>
          <td>{{ staff.username }}</td>
          <td>{{ staff.email }}</td>

          <td>
            <span
              class="badge"
              :class="staff.active ? 'bg-success' : 'bg-danger'"
            >
              {{ staff.active ? "Active" : "Inactive" }}
            </span>
          </td>

          <td>

            <button
              class="btn btn-danger btn-sm"
              @click="deactivateStaff(staff.id)"
              :disabled="!staff.active"
            >
              Deactivate
            </button>

          </td>

        </tr>

      </tbody>

    </table>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const staffs = ref([])
const searchKeyword = ref("")

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

import { useRouter } from "vue-router"

const router = useRouter()

function goDashboard() {
    router.push("/admin")
}

function goUsers() {
    router.push("/admin/users")
}

function goStaff() {
    router.push("/admin/staff")
}

function goTreks() {
    router.push("/admin/treks")
}

function goBookings() {
    router.push("/admin/bookings")
}

function logout() {
    localStorage.removeItem("token")
    router.push("/")
}

async function loadStaff(){

    const response = await axios.get(
        "http://127.0.0.1:5000/admin/staff",
        { headers }
    )

    staffs.value = response.data
}

async function searchStaff(){

    try{

        if(searchKeyword.value.trim() === ""){

            loadStaff()
            return

        }

        const response = await axios.get(

            `http://127.0.0.1:5000/search/staff?q=${searchKeyword.value}`,

            { headers }

        )

        staffs.value = response.data

    }

    catch(error){

        alert(error.response?.data?.message || "Server Error")

    }

}

async function deactivateStaff(id){

    await axios.put(
        `http://127.0.0.1:5000/admin/deactivate-staff/${id}`,
        {},
        { headers }
    )

    loadStaff()
}

onMounted(()=>{
    loadStaff()
})
</script>