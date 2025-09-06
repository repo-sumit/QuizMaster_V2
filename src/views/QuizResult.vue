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
        <router-link :to="`/user/subject/${quiz.subject_id}`" class="text-primary">{{ quiz.subject_name
          }}</router-link> /
        <router-link :to="`/user/chapter/${quiz.chapter_id}`" class="text-success">{{ quiz.chapter_name
          }}</router-link> /
        {{ quiz.title }} - Results
      </h1>
      <router-link :to="`/user/chapter/${quiz.chapter_id}`" class="btn btn-secondary">
        <i class="fas fa-arrow-left"></i> Back to Chapter
      </router-link>
    </div>

    <div v-if="score.total_questions === 0" class="alert alert-warning">
      This quiz had no questions to score.
    </div>

    <div class="row">
      <div class="col-lg-6">
        <!-- Score Card -->
        <div class="card shadow mb-4">
          <div class="card-header py-3 bg-primary text-white">
            <h6 class="m-0 font-weight-bold">Your Score</h6>
          </div>
          <div class="card-body text-center">
            <div
              :class="['display-4', 'font-weight-bold', score.percentage >= 70 ? 'text-success' : 'text-danger']">
              {{ score.score }}/{{ score.total_questions }}
            </div>
            <div class="mt-3">
              <span :class="['badge', score.percentage >= 70 ? 'bg-success' : 'bg-danger']">
                {{ score.percentage >= 70 ? 'Passed' : 'Failed' }}
              </span>
              <p class="mt-2">Attempted on: {{ formatDate(score.timestamp) }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-6">
        <!-- Performance Summary -->
        <div class="card shadow mb-4">
          <div class="card-header py-3 bg-info text-white">
            <h6 class="m-0 font-weight-bold">Performance Summary</h6>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <h6>Percentage: {{ score.percentage }}%</h6>
              <div class="progress">
                <div :class="['progress-bar', score.percentage >= 70 ? 'bg-success' : 'bg-danger']"
                  role="progressbar" :style="{ width: score.percentage + '%' }" :aria-valuenow="score.percentage"
                  aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            </div>
            <div>
              <router-link to="/user/scores" class="btn btn-primary">
                <i class="fas fa-history"></i> View All Attempts
              </router-link>
              <router-link :to="`/user/quiz/${quiz.id}`" class="btn btn-secondary">
                <i class="fas fa-redo"></i> Try Again
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Question Review -->
    <div class="card shadow mb-4">
      <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Question Review</h6>
      </div>
      <div class="card-body">
        <div v-for="(question, index) in quiz.questions" :key="question.id"
          :class="['mb-4', 'p-3', user_answers[question.id] == question.correct_option ? 'bg-success bg-opacity-10' : 'bg-danger bg-opacity-10']">
          <h6>Question {{ index + 1 }}: {{ question.question_statement }}</h6>
          <div class="mb-2">
            <div :class="['form-check', question.correct_option == 1 ? 'text-success font-weight-bold' : '']">
              <input class="form-check-input" type="radio" disabled :checked="user_answers[question.id] == '1'">
              <label class="form-check-label">
                {{ question.option1 }}
                <span v-if="question.correct_option == 1">(Correct)</span>
              </label>
            </div>
          </div>
          <div class="mb-2">
            <div :class="['form-check', question.correct_option == 2 ? 'text-success font-weight-bold' : '']">
              <input class="form-check-input" type="radio" disabled :checked="user_answers[question.id] == '2'">
              <label class="form-check-label">
                {{ question.option2 }}
                <span v-if="question.correct_option == 2">(Correct)</span>
              </label>
            </div>
          </div>
          <div v-if="question.option3" class="mb-2">
            <div :class="['form-check', question.correct_option == 3 ? 'text-success font-weight-bold' : '']">
              <input class="form-check-input" type="radio" disabled :checked="user_answers[question.id] == '3'">
              <label class="form-check-label">
                {{ question.option3 }}
                <span v-if="question.correct_option == 3">(Correct)</span>
              </label>
            </div>
          </div>
          <div v-if="question.option4" class="mb-2">
            <div :class="['form-check', question.correct_option == 4 ? 'text-success font-weight-bold' : '']">
              <input class="form-check-input" type="radio" disabled :checked="user_answers[question.id] == '4'">
              <label class="form-check-label">
                {{ question.option4 }}
                <span v-if="question.correct_option == 4">(Correct)</span>
              </label>
            </div>
          </div>
          <div :class="['mt-2', user_answers[question.id] == question.correct_option ? 'text-success' : 'text-danger']">
            <i :class="['fas', user_answers[question.id] == question.correct_option ? 'fa-check' : 'fa-times']"></i>
            {{ user_answers[question.id] == question.correct_option ? 'You answered correctly!' : 'Your answer was incorrect' }}
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
  name: 'UserQuizResults',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const quiz = ref({ id: '', title: '', chapter_id: '', chapter_name: '', subject_id: '', subject_name: '', questions: [] });
    const score = ref({ score: 0, total_questions: 0, timestamp: '', percentage: 0 });
    const user_answers = ref({});

    const fetchQuizResults = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/user/quizzes/${route.params.id}/results/${route.params.score_id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data = await response.json();
          quiz.value = data.quiz;
          score.value = data.score;
          user_answers.value = data.user_answers;
        } else {
          console.error('Failed to fetch quiz results:', await response.json());
          if (response.status === 401) {
            router.push('/login');
          }
        }
      } catch (error) {
        console.error('Error fetching quiz results:', error);
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

    fetchQuizResults();

    return {
      quiz,
      score,
      user_answers,
      formatDate,
      logout
    };
  },
};
</script>

<style scoped>
.bg-opacity-10 {
  background-color: rgba(0, 0, 0, 0.1);
}
</style>