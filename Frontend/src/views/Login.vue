<template>
  <div class="container mt-5">
    <div class="row justify-content-center">

      <div class="col-md-5">

        <div class="card shadow">

          <div class="card-header text-center">
            <h3>Trekking Management Application</h3>
          </div>

          <div class="card-body">

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
              class="btn btn-primary w-100"
              @click="loginUser"
            >
              Login
            </button>

            <p class="text-danger mt-3 text-center">
              {{ error }}
            </p>

            <hr>

            <p class="text-center">
              Don't have an account?

              <router-link to="/register">
                Register
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

const email = ref("")
const password = ref("")
const error = ref("")

async function loginUser() {

    error.value = ""

    try {

        const response = await axios.post(
            "http://127.0.0.1:5000/login",
            {
                email: email.value,
                password: password.value
            }
        )

        localStorage.setItem(
            "token",
            response.data.access_token
        )

        localStorage.setItem(
            "role",
            response.data.role
        )

        localStorage.setItem(
            "username",
            response.data.username
        )

        if(response.data.role === "admin"){
            router.push("/admin")
        }

        else if(response.data.role === "staff"){
            router.push("/staff")
        }

        else{
            router.push("/user")
        }

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