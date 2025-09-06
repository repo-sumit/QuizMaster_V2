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
        <h1 class="h3 mb-0 text-gray-800">Welcome, {{ user.full_name }}</h1>
        <div>
          <form class="d-inline" @submit.prevent="search">
            <div class="input-group">
              <input type="text" class="form-control" v-model="query" placeholder="Search...">
              <button class="btn btn-primary" type="submit">
                <i class="fas fa-search"></i>
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Score Summary -->
      <div class="row">
        <div class="col-xl-6 mb-4">
          <div class="card border-left-primary shadow h-100 py-2">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                    Quiz Attempts
                  </div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">
                    {{ total_attempts }}
                  </div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-6 mb-4">
          <div class="card border-left-success shadow h-100 py-2">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                    Average Score
                  </div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">
                    {{ avg_score.toFixed(2) }}%
                  </div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-chart-line fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Search Results or Normal View -->
      <div v-if="query" class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">Search Results for "{{ query }}"</h6>
        </div>
        <div class="card-body">
          <div v-if="filteredResults.subjects.length || filteredResults.chapters.length || filteredResults.quizzes.length">
            <!-- Subjects Results -->
            <div v-if="filteredResults.subjects.length">
              <h5>Subjects</h5>
              <div class="row">
                <div v-for="subject in filteredResults.subjects" :key="subject.id" class="col-lg-4 mb-4">
                  <div class="card h-100">
                    <div class="card-body">
                      <h5 class="card-title">{{ subject.name }}</h5>
                      <p class="card-text">{{ truncate(subject.description, 100) }}</p>
                      <router-link :to="`/user/subject/${subject.id}`" class="btn btn-primary">
                        View Chapters
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- Chapters Results -->
            <div v-if="filteredResults.chapters.length" class="mt-4">
              <h5>Chapters</h5>
              <div class="list-group">
                <router-link v-for="chapter in filteredResults.chapters" :key="chapter.id" :to="`/user/chapter/${chapter.id}`"
                             class="list-group-item list-group-item-action">
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ chapter.name }}</h6>
                    <small>{{ chapter.subject.name }}</small>
                  </div>
                  <p class="mb-1">{{ truncate(chapter.description, 100) }}</p>
                </router-link>
              </div>
            </div>
            <!-- Quizzes Results -->
            <div v-if="filteredResults.quizzes.length" class="mt-4">
              <h5>Quizzes</h5>
              <div class="list-group">
                <router-link v-for="quiz in filteredResults.quizzes" :key="quiz.id" :to="`/user/quiz/${quiz.id}`"
                             class="list-group-item list-group-item-action">
                  <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">{{ quiz.title }}</h6>
                    <small>{{ quiz.chapter.subject.name }} / {{ quiz.chapter.name }}</small>
                  </div>
                  <p class="mb-1">{{ truncate(quiz.remarks, 100) }}</p>
                  <small>Duration: {{ quiz.time_duration }}</small>
                </router-link>
              </div>
            </div>
          </div>
          <div v-else class="alert alert-info">
            No results found for "{{ query }}"
          </div>
        </div>
      </div>
      <!-- Normal Subjects List -->
      <div v-else class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">Available Subjects</h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div v-for="subject in subjects" :key="subject.id" class="col-lg-4 mb-4">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">{{ subject.name }}</h5>
                  <p class="card-text">{{ truncate(subject.description, 100) }}</p>
                  <router-link :to="`/user/subject/${subject.id}`" class="btn btn-primary">
                    View Chapters
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
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'UserDashboard',
  setup() {
    const router = useRouter();
    const user = ref({ full_name: '' });
    const total_attempts = ref(0);
    const avg_score = ref(0);
    const query = ref('');
    const subjects = ref([]);

    const fetchUserData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/dashboard/user', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data = await response.json();
          user.value = data.user;
          total_attempts.value = data.total_attempts || 0;
          avg_score.value = data.avg_score || 0;
        } else {
          console.error('Failed to fetch user data');
          if (response.status === 401) {
            router.push('/login');
          }
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    const fetchSubjects = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/subjects', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          subjects.value = await response.json();
        } else {
          console.error('Failed to fetch subjects');
          if (response.status === 401) {
            router.push('/login');
          }
        }
      } catch (error) {
        console.error('Error fetching subjects:', error);
      }
    };

    const filteredResults = computed(() => {
      if (!query.value) {
        return { subjects: subjects.value, chapters: [], quizzes: [] };
      }
      const searchTerm = query.value.toLowerCase();
      const filteredSubjects = subjects.value.filter(subject =>
        subject.name.toLowerCase().includes(searchTerm) ||
        subject.description.toLowerCase().includes(searchTerm)
      );
      const filteredChapters = [];
      const filteredQuizzes = [];

      subjects.value.forEach(subject => {
        // Filter chapters
        (subject.chapters || []).forEach(chapter => {
          if (
            chapter.name.toLowerCase().includes(searchTerm) ||
            chapter.description.toLowerCase().includes(searchTerm)
          ) {
            filteredChapters.push({ ...chapter, subject: { name: subject.name } });
          }
          // Filter quizzes
          (chapter.quizzes || []).forEach(quiz => {
            if (
              quiz.title.toLowerCase().includes(searchTerm) ||
              quiz.remarks.toLowerCase().includes(searchTerm)
            ) {
              filteredQuizzes.push({ ...quiz, chapter: { name: chapter.name, subject: { name: subject.name } } });
            }
          });
        });
      });

      return {
        subjects: filteredSubjects,
        chapters: filteredChapters,
        quizzes: filteredQuizzes,
      };
    });

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };

    const truncate = (text, length) => {
      if (!text || text.length <= length) return text;
      return text.substring(0, length) + '...';
    };

    fetchUserData();
    fetchSubjects();

    return {
      user,
      total_attempts,
      avg_score,
      query,
      subjects,
      filteredResults,
      logout,
      truncate,
    };
  },
};
</script>

<style scoped>
/* Styles inherited from App.vue */
</style>