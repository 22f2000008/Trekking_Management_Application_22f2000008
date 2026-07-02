<template>
  <div class="container mt-4">

    <h2 class="mb-4">
      Manage Staff
    </h2>

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

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

async function loadStaff(){

    const response = await axios.get(
        "http://127.0.0.1:5000/admin/staff",
        { headers }
    )

    staffs.value = response.data
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