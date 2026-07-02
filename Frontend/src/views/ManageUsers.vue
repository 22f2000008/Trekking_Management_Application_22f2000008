<template>
  <div class="container mt-4">

    <h2 class="mb-4">
      Manage Users
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

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

async function loadUsers(){

    const response = await axios.get(
        "http://127.0.0.1:5000/admin/users",
        { headers }
    )

    users.value = response.data
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