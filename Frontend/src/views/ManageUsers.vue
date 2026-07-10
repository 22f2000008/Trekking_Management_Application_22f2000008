<template>
  <nav class="navbar navbar-dark bg-dark px-3 mb-3">

  <span class="navbar-brand">
    Manage Users
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
      Manage Users
    </h2>
    <div class="row mb-3">

  <div class="col-md-10">

    <input
      type="text"
      class="form-control"
      placeholder="Search user by username..."
      v-model="searchKeyword"
    >

  </div>

  <div class="col-md-2">

    <button
      class="btn btn-primary w-100"
      @click="searchUsers"
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

        <tr v-for="user in users" :key="user.id">

          <td>{{ user.id }}</td>

          <td>{{ user.username }}</td>

          <td>{{ user.email }}</td>

          <td>

            <span
              class="badge"
              :class="user.active ? 'bg-success' : 'bg-danger'"
            >
              {{ user.active ? "Active" : "Inactive" }}
            </span>

          </td>

          <td>

            <button
              class="btn btn-danger btn-sm"
              @click="deactivateUser(user.id)"
              :disabled="!user.active"
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

const users = ref([])
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

async function loadUsers(){

    const response = await axios.get(
        "http://127.0.0.1:5000/admin/users",
        { headers }
    )

    users.value = response.data
}

async function searchUsers(){

    try{

        // If search box is empty, load all users
        if(searchKeyword.value.trim() === ""){

            loadUsers()
            return

        }

        const response = await axios.get(

            `http://127.0.0.1:5000/search/users?q=${searchKeyword.value}`,

            { headers }

        )

        users.value = response.data

    }

    catch(error){

        alert(error.response?.data?.message || "Server Error")

    }

}

async function deactivateUser(id){

    await axios.put(
        `http://127.0.0.1:5000/admin/deactivate-user/${id}`,
        {},
        { headers }
    )

    loadUsers()

}

onMounted(()=>{
    loadUsers()
})

</script>