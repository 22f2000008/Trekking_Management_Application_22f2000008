<template>

<div class="container mt-4">

    <div class="card shadow">

        <div class="card-header text-center">
            <h3>Update Trek Status</h3>
        </div>

        <div class="card-body">

            <div class="mb-3">

                <label class="form-label">
                    Select Status
                </label>

                <select
                    class="form-select"
                    v-model="status"
                >

                    <option>Pending</option>
                    <option>Approved</option>
                    <option>Open</option>
                    <option>Closed</option>
                    <option>Completed</option>

                </select>

            </div>

            <button
                class="btn btn-success w-100"
                @click="updateStatus"
            >
                Update Status
            </button>

            <p class="text-success text-center mt-3">
                {{ message }}
            </p>

        </div>

    </div>

</div>

</template>

<script setup>

import axios from "axios"
import { ref } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()

const status = ref("Open")
const message = ref("")

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

async function updateStatus(){

    const response = await axios.put(

        `http://127.0.0.1:5000/staff/trek/${route.params.id}/status`,

        {
            status: status.value
        },

        { headers }

    )

    message.value = response.data.message

}

</script>