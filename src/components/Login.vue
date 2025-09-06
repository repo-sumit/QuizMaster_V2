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
    <div class="col-lg-6">
      <div class="card">
        <div class="card-header bg-white border-0">
          <h2 class="text-center mb-0">Login</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="form.username"
                required
              >
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="form.password"
                required
              >
            </div>
            <div class="d-grid gap-2">
              <button type="submit" class="btn btn-primary btn-lg">Login</button>
            </div>
          </form>
          <div class="text-center mt-3">
            <p>Don't have an account? <router-link to="/register">Register here</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.form)
        });
        const data = await response.json();
        if (response.ok) {
          console.log(data.user.is_admin);
          localStorage.setItem('user', JSON.stringify(data.user));
          localStorage.setItem('token', data.token);
          if (data.user.is_admin) {
            this.$router.push('/admin/dashboard');
          } else {
            this.$router.push('/user/dashboard');
          }
          // Optionally, trigger a session refresh in App.vue
          this.$emit('refresh-session');
        } else {
          // Handle error (e.g., show flash message)
          console.error('Login failed:', data.message);
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Styles inherited from App.vue */
</style>