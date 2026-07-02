<template>
  <div class="container mt-5">
    <div class="row justify-content-center">

      <div class="col-md-5">

        <div class="card shadow">

          <div class="card-header text-center">
            <h3>User Registration</h3>
          </div>

          <div class="card-body">

            <div class="mb-3">
              <label class="form-label">Username</label>
              <input
                type="text"
                class="form-control"
                v-model="username"
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Email</label>
              <input
                type="email"
                class="form-control"
                v-model="email"
              >
            </div>

            <div class="mb-3">
              <label class="form-label">Password</label>
              <input
                type="password"
                class="form-control"
                v-model="password"
              >
            </div>

            <button
              class="btn btn-success w-100"
              @click="registerUser"
            >
              Register
            </button>

            <p class="text-success text-center mt-3">
              {{ success }}
            </p>

            <p class="text-danger text-center">
              {{ error }}
            </p>

            <hr>

            <p class="text-center">
              Already have an account?

              <router-link to="/">
                Login
              </router-link>
            </p>

          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import { useRouter } from "vue-router"

const router = useRouter()

const username = ref("")
const email = ref("")
const password = ref("")

const success = ref("")
const error = ref("")

async function registerUser() {

    success.value = ""
    error.value = ""

    try {

        const response = await axios.post(
            "http://127.0.0.1:5000/register",
            {
                username: username.value,
                email: email.value,
                password: password.value
            }
        )

        success.value = response.data.message

        setTimeout(() => {
            router.push("/")
        }, 1500)

    }

    catch(err){

        if(err.response){
            error.value = err.response.data.message
        }

        else{
            error.value = "Server Error"
        }

    }

}
</script>