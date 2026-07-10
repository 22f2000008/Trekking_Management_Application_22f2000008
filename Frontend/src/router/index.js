import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import UserDashboard from '../views/UserDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import StaffDashboard from '../views/StaffDashboard.vue'
import Profile from '../views/Profile.vue'
import MyBookings from '../views/MyBookings.vue'
import ManageUsers from '../views/ManageUsers.vue'
import ManageStaff from '../views/ManageStaff.vue'
import ManageTreks from "../views/ManageTreks.vue"
import ViewBookings from "../views/ViewBookings.vue"
import Participants from "../views/Participants.vue"
import UpdateStatus from "../views/UpdateStatus.vue"
import CreateStaff from "../views/CreateStaff.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/user',
      name: 'user',
      component: UserDashboard
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard
    },
    {
      path: '/staff',
      name: 'staff',
      component: StaffDashboard
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
    },
    {
      path: '/my-bookings',
      name: 'my-bookings',
      component: MyBookings
    },
    {
    path: '/admin/users',
    name: 'manage-users',
    component: ManageUsers
    },
    {
    path: '/admin/staff',
    name: 'manage-staff',
    component: ManageStaff
   },
   {
    path:'/admin/treks',
    name:'manage-treks',
    component:ManageTreks
  },
  {
    path:'/admin/bookings',
    name:'view-bookings',
    component:ViewBookings
  },
  {
    path: "/participants",
    name: "participants",
    component: Participants
  },
  {
    path: "/update-status/:id",
    name: "update-status",
    component: UpdateStatus
  },
  {
    path: "/admin/create-staff",
    name: "create-staff",
    component: CreateStaff
  },
  ]
})

export default router