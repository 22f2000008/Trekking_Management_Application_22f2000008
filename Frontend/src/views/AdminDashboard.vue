<template>


  <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow">

    <div class="container-fluid">
      <span class="navbar-brand fw-bold fs-4">
        Admin Dashboard
      </span>

      <div class="ms-auto">

        <button
          class="btn btn-outline-light me-2"
          @click="goDashboard">

          Admin Dashboard

        </button>
        <button
          class="btn btn-outline-light me-2"
          @click="goUsers">

          Manage Users

        </button>

        <button
          class="btn btn-outline-light me-2"
          @click="goStaff">

          Manage Staff

        </button>

        <button
          class="btn btn-outline-light me-2"
          @click="goTreks">

          Manage Treks

        </button>

        <button
          class="btn btn-danger"
          @click="logout">

          Logout

        </button>

      </div>

    </div>

  </nav>


  <div class="container mt-4">

    <h2 class="text-center mb-4">
      Admin Dashboard
    </h2>

    <div class="row">

      <div class="col-md-3 mb-4">

        <div class="card text-center shadow">

          <div class="card-body">

            <h5>Total Users</h5>

            <h2>{{ users.length }}</h2>

          </div>

        </div>

      </div>

      <div class="col-md-3 mb-4">

        <div class="card text-center shadow">

          <div class="card-body">

            <h5>Total Staff</h5>

            <h2>{{ staff.length }}</h2>

          </div>

        </div>

      </div>

      <div class="col-md-3 mb-4">

        <div class="card text-center shadow">

          <div class="card-body">

            <h5>Total Treks</h5>

            <h2>{{ treks.length }}</h2>

          </div>

        </div>

      </div>

      <div class="col-md-3 mb-4">

        <div class="card text-center shadow">

          <div class="card-body">

            <h5>Total Bookings</h5>

            <h2>{{ bookings.length }}</h2>

          </div>

        </div>

      </div>

    </div>

    <hr>


    <div class="text-end mb-4">

      <button
        class="btn btn-dark"
        @click="router.push('/admin/create-staff')">

        Create Staff

      </button>

    </div>

    <div class="card shadow">

      <div class="card-header bg-primary text-white">

        <h4 class="mb-0">

          Recent Booking History

        </h4>

      </div>

      <div class="card-body p-0">

        <table class="table table-striped table-hover mb-0">

          <thead class="table-dark">

            <tr>

              <th>ID</th>
              <th>User</th>
              <th>Trek</th>
              <th>Booking Date</th>
              <th>Status</th>

            </tr>

          </thead>

          <tbody>

            <tr
              v-for="booking in bookings"
              :key="booking.id">

              <td>{{ booking.booking_id }}</td>

              <td>{{ booking.username }}</td>

              <td>{{ booking.trek_name }}</td>

              <td>{{ booking.booking_date }}</td>

              <td>

                <span
                  class="badge"

                  :class="{

                    'bg-success': booking.status=='Completed',

                    'bg-warning text-dark': booking.status=='Booked',

                    'bg-danger': booking.status=='Cancelled'

                  }">

                  {{ booking.status }}

                </span>

              </td>

            </tr>

            <tr v-if="bookings.length==0">

              <td colspan="5" class="text-center">

                No Bookings Found

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>

  </div>

</template>

<script setup>

import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import axios from "axios"

const router = useRouter()

// Reactive Variables

const users = ref([])
const staff = ref([])
const treks = ref([])
const bookings = ref([])

// JWT Token

const token = localStorage.getItem("token")

const headers = {

    Authorization: `Bearer ${token}`

}

// Navbar Navigation

function goUsers(){

    router.push("/admin/users")

}

function goStaff(){

    router.push("/admin/staff")

}

function goTreks(){

    router.push("/admin/treks")

}

function logout(){

    localStorage.removeItem("token")

    router.push("/")

}

// Load Dashboard Data

async function loadDashboard(){

    try{

        const usersResponse = await axios.get(

            "http://127.0.0.1:5000/admin/users",

            { headers }

        )

        users.value = usersResponse.data



        const staffResponse = await axios.get(

            "http://127.0.0.1:5000/admin/staff",

            { headers }

        )

        staff.value = staffResponse.data



        const treksResponse = await axios.get(

            "http://127.0.0.1:5000/admin/treks",

            { headers }

        )

        treks.value = treksResponse.data



        const bookingsResponse = await axios.get(

            "http://127.0.0.1:5000/admin/bookings",

            { headers }

        )

        bookings.value = bookingsResponse.data

    }

    catch(error){

        console.log(error)

        alert(

            error.response?.data?.message ||

            "Unable to load dashboard."

        )

    }

}

// Mounted

onMounted(() => {

    loadDashboard()

})

</script>

<style scoped>

/* ===========================
   Page
=========================== */

.container{
    padding-top:30px;
    padding-bottom:40px;
}

/* ===========================
   Navbar
=========================== */

.navbar{
    padding:15px 25px;
    box-shadow:0 4px 12px rgba(0,0,0,0.15);
}

.navbar-brand{
    font-size:26px;
    font-weight:bold;
    letter-spacing:0.5px;
}

.navbar .btn{
    border-radius:8px;
    font-weight:600;
    transition:0.3s;
}

.navbar .btn:hover{
    transform:translateY(-2px);
}

/* ===========================
   Dashboard Heading
=========================== */

h2{
    font-weight:700;
    color:#343a40;
    margin-bottom:30px;
}

/* ===========================
   Statistics Cards
=========================== */

.card{

    border:none;
    border-radius:15px;
    transition:.3s;
    overflow:hidden;
    height:100%;

}

.card:hover{

    transform:translateY(-8px);

    box-shadow:0 12px 25px rgba(0,0,0,.18)!important;

}

.card-body{

    padding:25px;

}

.card-body h5{

    font-weight:600;

}

.card-body h2{

    font-size:34px;

    font-weight:bold;

}

/* Different Colors */

.row .col-md-3:nth-child(1) .card{

    background:#0d6efd;

    color:white;

}

.row .col-md-3:nth-child(2) .card{

    background:#198754;

    color:white;

}

.row .col-md-3:nth-child(3) .card{

    background:#ffc107;

    color:black;

}

.row .col-md-3:nth-child(4) .card{

    background:#0dcaf0;

    color:black;

}

/* ===========================
   Create Staff Button
=========================== */

.text-end .btn{

    border-radius:8px;

    font-weight:600;

    padding:10px 25px;

}

/* ===========================
   Booking Card
=========================== */

.card-header{

    padding:15px;

}

.card-header h4{

    font-weight:700;

}

/* ===========================
   Table
=========================== */

.table{

    margin-bottom:0;

}

.table th{

    text-align:center;

    vertical-align:middle;

}

.table td{

    text-align:center;

    vertical-align:middle;

}

/* ===========================
   Badge
=========================== */

.badge{

    padding:8px 14px;

    font-size:13px;

    border-radius:20px;

}

/* ===========================
   Responsive
=========================== */

@media(max-width:768px){

    .navbar{

        text-align:center;

    }

    .navbar-brand{

        margin-bottom:12px;

    }

    .ms-auto{

        margin-top:10px;

    }

    .navbar .btn{

        margin-bottom:8px;

    }

    .text-end{

        text-align:center!important;

    }

}

</style>