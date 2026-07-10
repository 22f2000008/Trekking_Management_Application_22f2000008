<template>

  <div class="container mt-4">

    <h2 class="text-center mb-4">
      Create Trekking Staff
    </h2>

    <div class="card shadow">

      <div class="card-body">

        <form @submit.prevent="createStaff">

          <div class="mb-3">
            <label class="form-label">Username</label>
            <input
              type="text"
              class="form-control"
              v-model="staff.username"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              v-model="staff.email"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              v-model="staff.password"
              required
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Phone</label>
            <input
              type="text"
              class="form-control"
              v-model="staff.phone"
            >
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <textarea
              class="form-control"
              rows="3"
              v-model="staff.address"
            ></textarea>
          </div>

          <button class="btn btn-success w-100">
            Create Staff
          </button>

        </form>

      </div>

    </div>

  </div>

</template>

<script setup>

import { ref } from "vue"
import axios from "axios"

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

const staff = ref({
    username: "",
    email: "",
    password: "",
    phone: "",
    address: ""
})

async function createStaff(){

    try{

        await axios.post(
            "http://127.0.0.1:5000/admin/staff",
            staff.value,
            { headers }
        )

        alert("Staff created successfully!")

        staff.value = {
            username: "",
            email: "",
            password: "",
            phone: "",
            address: ""
        }

    }

    catch(error){

        alert(error.response?.data?.message || "Server Error")

    }

}

</script>