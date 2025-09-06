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
          <router-link :to="`/user/subject/${quiz.subject_id}`" class="text-primary text-decoration-none">{{ quiz.subject_name
            }}</router-link> /
          <router-link :to="`/user/chapter/${quiz.chapter_id}`" class="text-success text-decoration-none">{{ quiz.chapter_name
            }}</router-link> /
          {{ quiz.title }}
        </h1>
        <div class="quiz-timer">
          <i class="fas fa-clock"></i> Time: {{ quiz.time_duration }}
        </div>
      </div>

      <div class="card shadow mb-4">
        <div class="card-header py-3 bg-primary text-white">
          <h6 class="m-0 font-weight-bold">Quiz Instructions</h6>
        </div>
        <div class="card-body">
          <p>Please answer all questions. Each question has only one correct answer.</p>
          <p>Time Duration: {{ quiz.time_duration }}</p>
          <div v-if="quiz.remarks" class="alert alert-info">
            {{ quiz.remarks }}
          </div>
        </div>
      </div>

      <form @submit.prevent="submitQuiz">
        <div v-for="(question, index) in quiz.questions" :key="question.id" class="card question-card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">Question {{ index + 1 }}</h6>
          </div>
          <div class="card-body">
            <p class="font-weight-bold">{{ question.question_statement }}</p>
            <div class="form-group">
              <div class="form-check mb-2">
                <input class="form-check-input" type="radio" :name="`question_${question.id}`"
                  :id="`q${question.id}_option1`" value="1" v-model="answers[question.id]" required>
                <label class="form-check-label" :for="`q${question.id}_option1`">
                  {{ question.option1 }}
                </label>
              </div>
              <div class="form-check mb-2">
                <input class="form-check-input" type="radio" :name="`question_${question.id}`"
                  :id="`q${question.id}_option2`" value="2" v-model="answers[question.id]">
                <label class="form-check-label" :for="`q${question.id}_option2`">
                  {{ question.option2 }}
                </label>
              </div>
              <div v-if="question.option3" class="form-check mb-2">
                <input class="form-check-input" type="radio" :name="`question_${question.id}`"
                  :id="`q${question.id}_option3`" value="3" v-model="answers[question.id]">
                <label class="form-check-label" :for="`q${question.id}_option3`">
                  {{ question.option3 }}
                </label>
              </div>
              <div v-if="question.option4" class="form-check mb-2">
                <input class="form-check-input" type="radio" :name="`question_${question.id}`"
                  :id="`q${question.id}_option4`" value="4" v-model="answers[question.id]">
                <label class="form-check-label" :for="`q${question.id}_option4`">
                  {{ question.option4 }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="text-center mt-4 mb-5">
          <button type="submit" class="btn btn-primary btn-lg">
            <i class="fas fa-paper-plane"></i> Submit Quiz
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'UserQuiz',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const quiz = ref({ id: '', title: '', time_duration: '', remarks: '', chapter: { id: '', name: '', subject: { name: '' } }, questions: [] });
    const answers = ref({});

    const fetchQuiz = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${route.params.id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          quiz.value = await response.json();
        } else {
          console.error('Failed to fetch quiz:', await response.json());
        }
      } catch (error) {
        console.error('Error fetching quiz:', error);
      }
    };

    const submitQuiz = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${route.params.id}/submit`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ answers: answers.value }),
        });
        if (response.ok) {
          const data = await response.json();
          router.push(`/user/quiz/${route.params.id}/results/${data.score_id}`);
        } else {
          console.error('Failed to submit quiz:', await response.json());
        }
      } catch (error) {
        console.error('Error submitting quiz:', error);
      }
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };

    fetchQuiz();

    return {
      quiz,
      answers,
      submitQuiz,
      logout,
    };
  },
};
</script>

<style scoped>
.quiz-timer {
  font-size: 1.5rem;
  font-weight: bold;
  color: #e74a3b;
}

.question-card {
  border-left: 4px solid #4e73df;
  margin-bottom: 20px;
}
</style>