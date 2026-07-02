<template>

<div class="container mt-4">

    <h2 class="text-center mb-4">
        Staff Dashboard
    </h2>

    <div
        class="card shadow mb-4"
        v-for="trek in treks"
        :key="trek.id"
    >

        <div class="card-body">

            <h4>{{ trek.trek_name }}</h4>

            <p><b>Location:</b> {{ trek.location }}</p>

            <p><b>Difficulty:</b> {{ trek.difficulty }}</p>

            <p><b>Duration:</b> {{ trek.duration }} Days</p>

            <p><b>Available Slots:</b> {{ trek.available_slots }}</p>

            <p><b>Status:</b> {{ trek.status }}</p>

            <button
                class="btn btn-primary me-2"
                @click="viewParticipants(trek.id)"
            >
                Participants
            </button>

            <button
                class="btn btn-warning"
                @click="changeStatus(trek.id)"
            >
                Change Status
            </button>

        </div>

    </div>

</div>

</template>

<script setup>

import axios from "axios"
import { ref, onMounted } from "vue"

const treks = ref([])

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

async function loadTreks(){

    const response = await axios.get(
        "http://127.0.0.1:5000/staff/treks",
        { headers }
    )

    treks.value = response.data

}

import { useRouter } from "vue-router"

const router = useRouter()

function viewParticipants(id){

    router.push(`/participants/${id}`)

}

function changeStatus(id){

    router.push(`/update-status/${id}`)

}

onMounted(()=>{

    loadTreks()

})

</script>