<template>

<div class="container mt-4">

    <h2 class="mb-4 text-center">
        Trek Participants
    </h2>

    <table class="table table-bordered table-striped">

        <thead class="table-dark">

            <tr>
                <th>User ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Status</th>
            </tr>

        </thead>

        <tbody>

            <tr
                v-for="participant in participants"
                :key="participant.user_id"
            >

                <td>{{ participant.user_id }}</td>

                <td>{{ participant.username }}</td>

                <td>{{ participant.email }}</td>

                <td>{{ participant.booking_status }}</td>

            </tr>

        </tbody>

    </table>

</div>

</template>

<script setup>

import axios from "axios"
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()

const participants = ref([])

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

async function loadParticipants(){

    const response = await axios.get(

        `http://127.0.0.1:5000/staff/trek/${route.params.id}/participants`,

        { headers }

    )

    participants.value = response.data

}

onMounted(()=>{

    loadParticipants()

})

</script>