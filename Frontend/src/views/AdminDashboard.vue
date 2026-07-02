<template>
  <div class="container mt-4">

    <h2 class="text-center mb-4">
      Admin Dashboard
    </h2>

    <div class="row">

      <div class="col-md-3">
        <div class="card text-center shadow">
          <div class="card-body">
            <h5>Total Users</h5>
            <h2>{{ users.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-center shadow">
          <div class="card-body">
            <h5>Total Staff</h5>
            <h2>{{ staff.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-center shadow">
          <div class="card-body">
            <h5>Total Treks</h5>
            <h2>{{ treks.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-center shadow">
          <div class="card-body">
            <h5>Total Bookings</h5>
            <h2>{{ bookings.length }}</h2>
          </div>
        </div>
      </div>

    </div>

    <hr>

    <div class="d-grid gap-3">

    <button
    class="btn btn-primary"
    @click="router.push('/admin/users')"
>
    Manage Users
    </button>

    <button
    class="btn btn-success"
    @click="router.push('/admin/staff')"
>
    Manage Staff
    </button>

    <button
    class="btn btn-warning"
    @click="router.push('/admin/treks')"
>
    Manage Treks
    </button>

    <button
class="btn btn-info"
@click="router.push('/admin/bookings')"
>
View Bookings
</button>

    </div>

  </div>
</template>

<script setup>
import { useRouter } from "vue-router"

const router = useRouter()
import axios from "axios"
import { ref, onMounted } from "vue"

const users = ref([])
const staff = ref([])
const treks = ref([])
const bookings = ref([])

const token = localStorage.getItem("token")

const headers = {
    Authorization: `Bearer ${token}`
}

onMounted(async ()=>{

    try{

        users.value = (
            await axios.get(
                "http://127.0.0.1:5000/admin/users",
                {headers}
            )
        ).data

        staff.value = (
            await axios.get(
                "http://127.0.0.1:5000/admin/staff",
                {headers}
            )
        ).data

        treks.value = (
            await axios.get(
                "http://127.0.0.1:5000/admin/treks",
                {headers}
            )
        ).data

        bookings.value = (
            await axios.get(
                "http://127.0.0.1:5000/admin/bookings",
                {headers}
            )
        ).data

    }

    catch(error){
        console.log(error)
    }

})
</script>