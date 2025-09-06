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
    <div class="col-lg-8 text-center">
      <h1 class="display-4 mb-4">Welcome to <span class="text-primary">Quiz Master</span></h1>
      <p class="lead mb-5">
        Test your knowledge and prepare for exams with our comprehensive quiz platform.
        Choose from various subjects and chapters to begin your learning journey.
      </p>
      <div class="row g-4">
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-body">
              <h3 class="card-title">For Students</h3>
              <p class="card-text">
                Take quizzes, track your progress, and improve your knowledge.
              </p>
              <router-link to="/register" class="btn btn-primary">Register Now</router-link>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-body">
              <h3 class="card-title">Already Registered?</h3>
              <p class="card-text">
                Access your dashboard and continue your learning journey.
              </p>
              <router-link to="/login" class="btn btn-primary">Login</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
/* Styles are inherited from App.vue */
</style>