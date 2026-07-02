<template>

<div class="container mt-4">

<h2 class="mb-4">
All Bookings
</h2>

<table class="table table-bordered table-striped">

<thead class="table-dark">

<tr>

<th>Booking ID</th>

<th>User</th>

<th>Trek</th>

<th>Status</th>

</tr>

</thead>

<tbody>

<tr
v-for="booking in bookings"
:key="booking.booking_id"
>

<td>{{ booking.booking_id }}</td>

<td>{{ booking.username }}</td>

<td>{{ booking.trek_name }}</td>

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
import { ref,onMounted } from "vue"

const bookings=ref([])

const token=localStorage.getItem("token")

const headers={
Authorization:`Bearer ${token}`
}

async function loadBookings(){

const response=await axios.get(

"http://127.0.0.1:5000/admin/bookings",

{headers}

)

bookings.value=response.data

}

onMounted(()=>{

loadBookings()

})

</script>