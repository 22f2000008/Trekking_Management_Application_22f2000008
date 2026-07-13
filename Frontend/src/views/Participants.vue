<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">

        <div class="container-fluid">

            <span class="navbar-brand fw-bold">
                Staff Dashboard
            </span>

            <div class="ms-auto">

                <button
    class="btn btn-outline-light btn-sm me-2"
    @click="router.push('/staff')"
>
    Dashboard
</button>

<button
    class="btn btn-outline-light btn-sm me-2"
    @click="router.push('/participants')"
>
    Participants
</button>

<button
    class="btn btn-danger btn-sm"
    @click="logout"
>
    Logout
</button>


            </div>

        </div>

    </nav>


    <div class="container mt-4">

        <h2 class="text-center mb-4">

            Trek Participants

        </h2>

        <div class="card shadow">

            <div class="card-header bg-primary text-white">

                <h4 class="mb-0">

                    Registered Participants

                </h4>

            </div>

            <div class="card-body p-0">

                <table class="table table-hover table-striped mb-0">

                    <thead class="table-dark">

                        <tr>

                            <th>Trek</th>
                            <th>User ID</th>

                            <th>Username</th>

                            <th>Email</th>
                            <th>Booking Date</th>

                            <th>Status</th>

                        </tr>

                    </thead>

                    <tbody>

                        <tr
                            v-for="participant in participants"
                            :key="participant.user_id"
                        >

                            <td>{{ participant.trek_name }}</td>

                            <td>{{ participant.user_id }}</td>

                            <td>{{ participant.username }}</td>

                            <td>{{ participant.email }}</td>

                            <td>{{ participant.booking_date }}</td>

                            <td>

                                <span
                                    class="badge"

                                    :class="{

                                        'bg-success': participant.booking_status=='Completed',

                                        'bg-warning text-dark': participant.booking_status=='Booked',

                                        'bg-danger': participant.booking_status=='Cancelled'

                                    }"
                                >

                                    {{ participant.booking_status }}

                                </span>

                            </td>

                        </tr>

                        <tr v-if="participants.length==0">

                            <td colspan="4" class="text-center text-danger py-4">

                                No Participants Found

                            </td>

                        </tr>

                    </tbody>

                </table>

            </div>

        </div>

         

    </div>

</template>

<script setup>

import axios from "axios"
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const participants = ref([])

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

async function loadParticipants(){

    const response = await axios.get(

        "http://127.0.0.1:5000/staff/participants",

        { headers }

    )

    participants.value = response.data

}
function logout(){

    localStorage.removeItem("token")

    router.push("/")

}

onMounted(()=>{

    loadParticipants()

})

</script>