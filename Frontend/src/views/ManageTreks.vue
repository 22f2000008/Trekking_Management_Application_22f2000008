<template>
  <nav class="navbar navbar-dark bg-dark px-3 mb-3">

  <span class="navbar-brand">
    Manage Treks
  </span>

  <div>

    <button class="btn btn-outline-light me-2" @click="goDashboard">
      Dashboard
    </button>

    <button class="btn btn-outline-light me-2" @click="goUsers">
      Users
    </button>

    <button class="btn btn-outline-light me-2" @click="goStaff">
      Staff
    </button>

    <button class="btn btn-outline-light me-2" @click="goTreks">
      Treks
    </button>

    <button class="btn btn-outline-light me-2" @click="goBookings">
      Bookings
    </button>

    <button class="btn btn-danger" @click="logout">
      Logout
    </button>

  </div>

</nav>
  <div class="container mt-4">

    <h2 class="mb-4">Manage Treks</h2>
    <div class="row mb-4">

  <div class="col-md-10">

    <input
      type="text"
      class="form-control"
      placeholder="Search trek by name..."
      v-model="searchKeyword"
    >

  </div>

  <div class="col-md-2">

    <button
      class="btn btn-primary w-100"
      @click="searchTreks"
    >
      Search
    </button>

  </div>

</div>

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
          <th>Duration</th>
          <th>Slots</th>
          <th>Status</th>
          <th>Description</th>
          <th>Staff ID</th>
          <th>Assign Staff</th>
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

        <td>{{ trek.duration }}</td>

        <td>{{ trek.available_slots }}</td>
        <td>{{ trek.status }}</td>
        <td>{{ trek.description }}</td>
        <td>{{ trek.assigned_staff_id }}</td>


        <td>

            <select
                class="form-select mb-2"
                v-model="trek.assigned_staff_id"
            >

                <option disabled value="">
                    Select Staff
                </option>

                <option
                    v-for="staff in staffs"
                    :key="staff.id"
                    :value="staff.id"
                >
                    {{ staff.username }}
                </option>

            </select>

            <button
                class="btn btn-primary btn-sm w-100"
                @click="assignStaff(trek)"
            >
                Assign
            </button>

        </td>

    </tr>

</tbody>

    </table>

  </div>
</template>

<script setup>

import axios from "axios"
import { ref, onMounted } from "vue"

const treks = ref([])
const searchKeyword = ref("")
const staffs = ref([])

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
    Authorization: `Bearer ${token}`
}
import { useRouter } from "vue-router"

const router = useRouter()

function goDashboard() {
    router.push("/admin")
}

function goUsers() {
    router.push("/admin/users")
}

function goStaff() {
    router.push("/admin/staff")
}

function goTreks() {
    router.push("/admin/treks")
}

function goBookings() {
    router.push("/admin/bookings")
}

function logout() {
    localStorage.removeItem("token")
    router.push("/")
}

async function loadTreks(){

    const response = await axios.get(
        "http://127.0.0.1:5000/admin/treks",
        { headers }
    )

    treks.value = response.data

}

async function searchTreks(){

    try{

        if(searchKeyword.value.trim() === ""){

            await loadTreks()
            return

        }

        const response = await axios.get(

            `http://127.0.0.1:5000/search/treks?q=${searchKeyword.value}`,

            { headers }

        )

        console.log(response.data)

        treks.value = response.data

    }

    catch(error){
      console.log(error)


        alert(error.response?.data?.message || "Server Error")

    }

}


async function loadStaff(){

    const response = await axios.get(
        "http://127.0.0.1:5000/admin/staff",
        { headers }
    )

    staffs.value = response.data

}


async function createTrek(){

    try{

        await axios.post(
            "http://127.0.0.1:5000/admin/treks",
            trek.value,
            { headers }
        )

        alert("Trek created successfully!")

        await loadTreks()

        trek.value = {
            trek_name:"",
            location:"",
            difficulty:"Easy",
            duration:1,
            available_slots:10,
            start_date:"",
            end_date:"",
            description:""
        }

    }

    catch(error){

        alert(error.response?.data?.message || "Server Error")

    }

}


async function assignStaff(trek){

    try{

        await axios.put(

            `http://127.0.0.1:5000/admin/assign-staff/${trek.id}`,

            {
                staff_id: trek.assigned_staff_id
            },

            { headers }

        )

        alert("Staff assigned successfully!")

        await loadTreks()

    }

    catch(error){

        alert(error.response?.data?.message || "Server Error")

    }

}

onMounted(async ()=>{

    await loadTreks()
    await loadStaff()

})

</script>