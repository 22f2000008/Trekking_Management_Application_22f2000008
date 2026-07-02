<template>

<div class="container mt-4">

    <div class="card shadow">

        <div class="card-header text-center">
            <h3>My Profile</h3>
        </div>

        <div class="card-body">

            <div class="mb-3">
                <label class="form-label">Username</label>

                <input
                    type="text"
                    class="form-control"
                    v-model="username"
                >
            </div>

            <div class="mb-3">
                <label class="form-label">Email</label>

                <input
                    type="email"
                    class="form-control"
                    v-model="email"
                >
            </div>

            <button
                class="btn btn-primary w-100"
                @click="updateProfile"
            >
                Update Profile
            </button>

            <p class="text-success text-center mt-3">
                {{ message }}
            </p>

        </div>

    </div>

</div>

</template>

<script setup>

import { ref, onMounted } from "vue"
import axios from "axios"

const username = ref("")
const email = ref("")
const message = ref("")

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

async function loadProfile(){

    const response = await axios.get(
        "http://127.0.0.1:5000/profile",
        { headers }
    )

    username.value = response.data.username
    email.value = response.data.email

}

async function updateProfile(){

    const response = await axios.put(
        "http://127.0.0.1:5000/profile",
        {
            username: username.value,
            email: email.value
        },
        { headers }
    )

    message.value = response.data.message

}

onMounted(() => {

    loadProfile()

})

</script>