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
                Staff Dashboard
            </button>

            <button
                class="btn btn-outline-light btn-sm me-2"
                @click="goParticipants"
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
        Staff Dashboard
    </h2>

    <div class="row mb-4">

        <div class="col-md-4">

            <div class="card text-center shadow">

                <div class="card-body">

                    <h5>Assigned Treks</h5>

                    <h2>{{ treks.length }}</h2>

                </div>

            </div>

        </div>

        <div class="col-md-4">

            <div class="card text-center shadow">

                <div class="card-body">

                    <h5>Total Participants</h5>

                    <h2>{{ totalParticipants }}</h2>

                </div>

            </div>

        </div>

        <div class="col-md-4">

            <div class="card text-center shadow">

                <div class="card-body">

                    <h5>Open Treks</h5>

                    <h2>{{ openTreks }}</h2>

                </div>

            </div>

        </div>

    </div>


    <div class="card shadow">

        <div class="card-header bg-primary text-white">

            <h4 class="mb-0">
                My Assigned Treks
            </h4>

        </div>

        <div class="card-body p-0">

            <table class="table table-hover table-striped mb-0">

                <thead class="table-dark">

                    <tr>

                        <th>Trek Name</th>

                        <th>Start Date</th>

                        <th>Participants</th>

                        <th>Status</th>

                        <th>Action</th>

                    </tr>

                </thead>

                <tbody>

                    <tr
                        v-for="trek in treks"
                        :key="trek.id"
                    >

                        <td>{{ trek.trek_name }}</td>

                        <td>{{ trek.start_date }}</td>

                        <td>{{ trek.total_participants }}</td>

                        <td>{{ trek.status }}</td>

                        <td>

                            <button
                                class="btn btn-warning btn-sm"
                                @click="changeStatus(trek.id)"
                            >
                                Status
                            </button>

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
import { ref, onMounted, computed } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const treks = ref([])

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

async function loadTreks(){

    try{

        const response = await axios.get(
            "http://127.0.0.1:5000/staff/treks",
            { headers }
        )

        treks.value = response.data

    }

    catch(error){

        console.log(error)

        router.push("/")

    }

}

 

const totalParticipants = computed(() => {

    return treks.value.reduce(
        (total, trek) => total + trek.total_participants,
        0
    )

})

const openTreks = computed(() => {

    return treks.value.filter(
        trek => trek.status === "Open"
    ).length

})

 

function goParticipants(){

    router.push("/participants")

}

 

function changeStatus(id){

    router.push(`/update-status/${id}`)

}


function logout(){

    localStorage.removeItem("token")

    router.push("/")

}


onMounted(()=>{

    if(!token){

        router.push("/")

        return

    }

    loadTreks()

})

</script>