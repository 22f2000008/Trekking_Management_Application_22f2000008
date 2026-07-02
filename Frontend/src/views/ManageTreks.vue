<template>
  <div class="container mt-4">

    <h2 class="mb-4">Manage Treks</h2>

    <form @submit.prevent="createTrek" class="mb-5">

      <div class="row">

        <div class="col-md-6 mb-3">
          <input
            v-model="trek.trek_name"
            class="form-control"
            placeholder="Trek Name"
            required
          >
        </div>

        <div class="col-md-6 mb-3">
          <input
            v-model="trek.location"
            class="form-control"
            placeholder="Location"
            required
          >
        </div>

        <div class="col-md-6 mb-3">
          <select
            v-model="trek.difficulty"
            class="form-select"
          >
            <option>Easy</option>
            <option>Moderate</option>
            <option>Hard</option>
          </select>
        </div>

        <div class="col-md-6 mb-3">
          <input
            type="number"
            v-model="trek.duration"
            class="form-control"
            placeholder="Duration"
          >
        </div>

        <div class="col-md-6 mb-3">
          <input
            type="number"
            v-model="trek.available_slots"
            class="form-control"
            placeholder="Available Slots"
          >
        </div>

        <div class="col-md-6 mb-3">
          <input
            type="date"
            v-model="trek.start_date"
            class="form-control"
          >
        </div>

        <div class="col-md-6 mb-3">
          <input
            type="date"
            v-model="trek.end_date"
            class="form-control"
          >
        </div>

        <div class="col-md-12 mb-3">
          <textarea
            v-model="trek.description"
            class="form-control"
            placeholder="Description"
          ></textarea>
        </div>

      </div>

      <button class="btn btn-success">
        Create Trek
      </button>

    </form>

    <hr>

    <table class="table table-bordered">

      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Location</th>
          <th>Difficulty</th>
          <th>Slots</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="trek in treks"
          :key="trek.id"
        >

          <td>{{ trek.id }}</td>
          <td>{{ trek.trek_name }}</td>
          <td>{{ trek.location }}</td>
          <td>{{ trek.difficulty }}</td>
          <td>{{ trek.available_slots }}</td>
          <td>{{ trek.status }}</td>

        </tr>

      </tbody>

    </table>

  </div>
</template>

<script setup>

import axios from "axios"
import { ref, onMounted } from "vue"

const treks = ref([])

const trek = ref({
    trek_name:"",
    location:"",
    difficulty:"Easy",
    duration:1,
    available_slots:10,
    start_date:"",
    end_date:"",
    description:""
})

const token = localStorage.getItem("token")

const headers = {
    Authorization:`Bearer ${token}`
}

async function loadTreks(){

    const response = await axios.get(
        "http://127.0.0.1:5000/admin/treks",
        {headers}
    )

    treks.value = response.data
}

async function createTrek(){

    await axios.post(
        "http://127.0.0.1:5000/admin/treks",
        trek.value,
        {headers}
    )

    loadTreks()
}

onMounted(()=>{
    loadTreks()
})

</script>