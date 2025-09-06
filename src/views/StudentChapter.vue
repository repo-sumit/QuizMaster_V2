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
        <h1 class="h3 mb-0 text-gray-800">
          <router-link :to="`/user/subject/${chapter.subject_id}`" class="text-primary text-decoration-none">{{ chapter.subject_name
            }}</router-link> /
          {{ chapter.name }}
        </h1>
        <router-link :to="`/user/subject/${chapter.subject_id}`" class="btn btn-secondary">
        <i class="fas fa-arrow-left"></i> Back to Subject
      </router-link>
      </div>

      <div class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">Available Quizzes</h6>
        </div>
        <div class="card-body">
          <div class="list-group">
            <div v-for="quiz in chapter.quizzes" :key="quiz.id" class="list-group-item">
              <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">{{ quiz.title }}</h5>
                <small>Duration: {{ quiz.time_duration }}</small>
              </div>
              <p class="mb-1">{{ quiz.remarks }}</p>
              <div class="d-flex justify-content-between align-items-center mt-2">
                <small>Date: {{ quiz.date_of_quiz }}</small>
                <router-link :to="`/user/quiz/${quiz.id}`" class="btn btn-sm btn-primary">
                  Take Quiz
                </router-link>
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
  name: 'UserChapter',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const chapter = ref({ id: '', name: '', subject: { id: '', name: '' }, quizzes: [] });

    const fetchChapter = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/chapters/${route.params.id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          chapter.value = await response.json();
        } else {
          console.error('Failed to fetch chapter');
        }
      } catch (error) {
        console.error('Error fetching chapter:', error);
      }
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };

    fetchChapter();

    return {
      chapter,
      logout
    };
  },
};
</script>

<style scoped>
/* Styles inherited from App.vue */
</style>