<template>

<div class="container mt-4">

<h2 class="mb-4 text-center">
Available Treks
</h2>
<div class="mb-4">

<button
class="btn btn-primary me-2"
@click="router.push('/my-bookings')"
>
My Bookings
</button>

<button
class="btn btn-secondary"
@click="router.push('/profile')"
>
Profile
</button>

</div>

<div class="row">

<div
class="col-md-4 mb-4"
v-for="trek in treks"
:key="trek.id"
>

<div class="card shadow h-100">

<div class="card-body">

<h4>{{ trek.trek_name }}</h4>

<p><b>Location:</b> {{ trek.location }}</p>

<p><b>Difficulty:</b> {{ trek.difficulty }}</p>

<p><b>Duration:</b> {{ trek.duration }} Days</p>

<p><b>Slots:</b> {{ trek.available_slots }}</p>

<p><b>Status:</b> {{ trek.status }}</p>

<button
class="btn btn-success w-100"
@click="bookTrek(trek.id)"
>
Book Trek
</button>

</div>

</div>

</div>

</div>

</div>

</template>

<script setup>

import axios from "axios"
import { ref,onMounted } from "vue"
import { useRouter } from "vue-router"

const treks=ref([])
const router = useRouter()

const token=localStorage.getItem("token")

const headers={
Authorization:`Bearer ${token}`
}

async function loadTreks(){

const response=await axios.get(
"http://127.0.0.1:5000/treks",
{headers}
)

treks.value=response.data

}

async function bookTrek(id){

try{

await axios.post(

"http://127.0.0.1:5000/bookings",

{
trek_id:id
},

{headers}

)

alert("Booking Successful!")

loadTreks()

}

catch(error){

alert(error.response.data.message)

}

}

onMounted(()=>{

loadTreks()

})

</script>