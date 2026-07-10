<template>

<nav class="navbar navbar-dark bg-dark px-3 mb-3">

    <span class="navbar-brand">
        Trekking Management Application
    </span>

    <div>

        <button
            class="btn btn-outline-light me-2"
            @click="router.push('/user')"
        >
            User Dashboard
        </button>

        <button
            class="btn btn-outline-light me-2"
            @click="router.push('/my-bookings')"
        >
            My Bookings
        </button>

        <button
            class="btn btn-outline-light btn-sm me-2"
            @click="router.push('/profile')"
        >
            Profile
        </button>

        <button
            class="btn btn-danger"
            @click="logout"
        >
            Logout
        </button>

    </div>

</nav>

<div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">

        <h2>
            My Bookings
        </h2>

        <button
            class="btn btn-success"
            @click="exportBookings"
        >
             Export Booking History
        </button>

    </div>

    <table class="table table-bordered table-striped">

        <thead class="table-dark">

            <tr>

                <th>Booking ID</th>
                <th>Trek</th>
                <th>Location</th>
                <th>Booking Date</th>
                <th>Status</th>

            </tr>

        </thead>

        <tbody>

            <tr
                v-for="booking in bookings"
                :key="booking.booking_id"
            >

                <td>{{ booking.booking_id }}</td>
                <td>{{ booking.trek_name }}</td>
                <td>{{ booking.location }}</td>
                <td>{{ booking.booking_date }}</td>

                <td>

                    <span class="badge bg-success">

                        {{ booking.status }}

                    </span>

                </td>

            </tr>

        </tbody>

    </table>

</div>

</template>

<script setup>

import axios from "axios"
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const bookings = ref([])

const token = localStorage.getItem("token")

const headers = {

    Authorization: `Bearer ${token}`

}

function logout() {

    localStorage.removeItem("token")

    router.push("/")

}

async function loadBookings() {

    try {

        const response = await axios.get(

            "http://127.0.0.1:5000/my-bookings",

            { headers }

        )

        bookings.value = response.data

    }

    catch (error) {

        alert(

            error.response?.data?.message ||

            "Unable to load bookings."

        )

    }

}

async function exportBookings() {

    try {

        const response = await axios.post(

            "http://127.0.0.1:5000/export-bookings",

            {},

            { headers }

        )

        alert(response.data.message)

    }

    catch (error) {

        alert(

            error.response?.data?.message ||

            "Unable to export booking history."

        )

    }

}

onMounted(() => {

    loadBookings()

})

</script>