<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/user/dashboard">
          <span class="text-primary">Quiz</span>Master
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/user/scores">History</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <button class="btn btn-danger ms-2" @click="logout">
                <i class="fas fa-sign-out-alt"></i> Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container-fluid p-5">
      <div class="d-sm-flex align-items-center justify-content-between mb-4">
        <h1 class="h3 mb-0 text-gray-800">{{ subject.name }}</h1>
        <router-link to="/user/dashboard" class="btn btn-secondary">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </router-link>
      </div>

      <div class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">Chapters</h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div v-for="chapter in subject.chapters" :key="chapter.id" class="col-lg-6 mb-4">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">{{ chapter.name }}</h5>
                  <p class="card-text">{{ chapter.description }}</p>
                  <router-link :to="`/user/chapter/${chapter.id}`" class="btn btn-primary">
                    View Quizzes
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'UserSubject',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const subject = ref({ id: '', name: '', chapters: [] });

    const fetchSubject = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${route.params.id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          subject.value = await response.json();
        } else {
          console.error('Failed to fetch subject');
        }
      } catch (error) {
        console.error('Error fetching subject:', error);
      }
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };

    fetchSubject();

    return {
      subject,
      logout
    };
  },
};
</script>

<style scoped>
/* Styles inherited from App.vue */
</style>