<template>
      <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container">
        <router-link class="navbar-brand" to="/">
          <span class="text-primary">Quiz</span>Master
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">Register</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  <div class="row justify-content-center mt-5">
    <div class="col-lg-8">
      <div class="card">
        <div class="card-header bg-white border-0">
          <h2 class="text-center mb-0">Create Your Account</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleRegister">
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="username" class="form-label">Username (Email)</label>
                <input
                  type="email"
                  class="form-control"
                  id="username"
                  v-model="form.username"
                  required
                >
              </div>
              <div class="col-md-6 mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="password"
                  v-model="form.password"
                  required
                >
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="full_name" class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="full_name"
                  v-model="form.full_name"
                  required
                >
              </div>
              <div class="col-md-6 mb-3">
                <label for="qualification" class="form-label">Qualification</label>
                <input
                  type="text"
                  class="form-control"
                  id="qualification"
                  v-model="form.qualification"
                >
              </div>
            </div>
            <div class="mb-3">
              <label for="dob" class="form-label">Date of Birth</label>
              <input
                type="date"
                class="form-control"
                id="dob"
                v-model="form.dob"
              >
            </div>
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg">Register</button>
            </div>
          </form>
          <div class="text-center mt-3">
            <p>Already have an account? <router-link to="/login">Login here</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        password: '',
        full_name: '',
        qualification: '',
        dob: '',
      },
    };
  },
  methods: {
    async handleRegister() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form),
        });
        const data = await response.json();
        if (response.ok) {
          this.$router.push('/login');
        } else {
          // Handle error (e.g., show flash message)
          console.error('Registration failed:', data.message);
        }
      } catch (error) {
        console.error('Error during registration:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Styles inherited from App.vue */
</style>