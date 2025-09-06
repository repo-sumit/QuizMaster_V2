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
        <h1 class="h3 mb-0 text-gray-800">My Quiz Attempts</h1>
        <router-link to="/user/dashboard" class="btn btn-secondary">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </router-link>
      </div>

      <div class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">Quiz History</h6>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Quiz</th>
                  <th>Chapter</th>
                  <th>Subject</th>
                  <th>Score</th>
                  <th>Date</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="score in scores" :key="score.id">
                  <td>{{ score.quiz_title }}</td>
                  <td>{{ score.chapter_name }}</td>
                  <td>{{ score.subject_name }}</td>
                  <td>
                    <span :class="score.percentage >= 70 ? 'text-success' : 'text-danger'">
                      {{ score.score }}/{{ score.total_questions }}
                    </span>
                  </td>
                  <td>{{ formatDate(score.timestamp) }}</td>
                  <td>
                    <router-link :to="`/user/quiz/${score.quiz_id}/results/${score.id}`"
                      class="btn btn-sm btn-info">
                      <i class="fas fa-eye"></i> View
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'StudentScores',
  setup() {
    const router = useRouter();
    const scores = ref([]);
    const token = localStorage.getItem('token') || '';

    const fetchScores = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/user/scores', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          scores.value = await response.json();
        } else {
          console.error('Failed to fetch scores:', await response.json());
          if (response.status === 401) {
            router.push('/login');
          }
        }
      } catch (error) {
        console.error('Error fetching scores:', error);
      }
    };

    const formatDate = (timestamp) => {
      const date = new Date(timestamp);
      return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      }).replace(',', '');
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };

    fetchScores();

    return {
      scores,
      formatDate,
      logout,
    };
  },
};
</script>

<style scoped>
/* Styles inherited from App.vue */
</style>