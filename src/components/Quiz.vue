<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/admin/dashboard">
          <span class="text-primary">Quiz</span>Master
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
             <router-link class="nav-link" to="/admin/stats">Stats</router-link>
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
          <router-link :to="`/admin/subject/${quiz.subject_id}`" class="text-primary text-decoration-none">{{ quiz.subject_name
            }}</router-link> /
          <router-link :to="`/admin/chapter/${quiz.chapter_id}`" class="text-success text-decoration-none">{{ quiz.chapter_name
          }}</router-link> /
          {{ quiz.title }}
        </h1>
        <div>
          <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editQuizModal">
            <i class="fas fa-edit"></i> Edit Quiz
          </button>
          <router-link :to="`/admin/chapter/${quiz.chapter_id}`" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to Quizzes
          </router-link>
        </div>
      </div>

      <div class="card shadow mb-4">
        <div class="card-header py-3 bg-warning">
          <h6 class="m-0 font-weight-bold text-white">Quiz Details</h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-4">
              <p><strong>Date:</strong> {{ quiz.date_of_quiz }}</p>
            </div>
            <div class="col-md-4">
              <p><strong>Duration:</strong> {{ quiz.time_duration }}</p>
            </div>
            <div class="col-md-4">
              <p><strong>Questions:</strong> {{ quiz.questions.length }}</p>
            </div>
          </div>
          <div v-if="quiz.remarks" class="alert alert-light">
            {{ quiz.remarks }}
          </div>
          <div class="mt-4">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="font-weight-bold">Questions</h5>
              <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createQuestionModal">
                <i class="fas fa-plus"></i> Add Question
              </button>
            </div>
            <div v-for="(question, index) in quiz.questions" :key="question.id" class="card question-item mb-3">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                  <div class="w-75">
                    <h6 class="font-weight-bold">Q{{ index + 1 }}. {{ question.question_statement }}</h6>
                    <div class="options mt-2">
                      <div class="option mb-1" :class="{ 'correct-option': question.correct_option == 1 }">
                        <strong>1.</strong> {{ question.option1 }}
                      </div>
                      <div class="option mb-1" :class="{ 'correct-option': question.correct_option == 2 }">
                        <strong>2.</strong> {{ question.option2 }}
                      </div>
                      <div v-if="question.option3" class="option mb-1"
                        :class="{ 'correct-option': question.correct_option == 3 }">
                        <strong>3.</strong> {{ question.option3 }}
                      </div>
                      <div v-if="question.option4" class="option mb-1"
                        :class="{ 'correct-option': question.correct_option == 4 }">
                        <strong>4.</strong> {{ question.option4 }}
                      </div>
                    </div>
                  </div>
                  <div>
                    <button class="btn btn-sm btn-info" data-bs-toggle="modal"
                      :data-bs-target="`#editQuestionModal${question.id}`">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" @click="deleteQuestion(question.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Question Modal -->
      <div class="modal fade" id="createQuestionModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add New Question</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="createQuestion">
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Question Statement</label>
                  <textarea class="form-control" v-model="newQuestion.question_statement" rows="3" required></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Options</label>
                  <div class="input-group mb-2">
                    <span class="input-group-text">1</span>
                    <input type="text" class="form-control" v-model="newQuestion.option1" required>
                    <span class="input-group-text">
                      <input class="form-check-input" type="radio" v-model="newQuestion.correct_option" value="1"
                        checked>
                    </span>
                  </div>
                  <div class="input-group mb-2">
                    <span class="input-group-text">2</span>
                    <input type="text" class="form-control" v-model="newQuestion.option2" required>
                    <span class="input-group-text">
                      <input class="form-check-input" type="radio" v-model="newQuestion.correct_option" value="2">
                    </span>
                  </div>
                  <div class="input-group mb-2">
                    <span class="input-group-text">3</span>
                    <input type="text" class="form-control" v-model="newQuestion.option3">
                    <span class="input-group-text">
                      <input class="form-check-input" type="radio" v-model="newQuestion.correct_option" value="3">
                    </span>
                  </div>
                  <div class="input-group mb-2">
                    <span class="input-group-text">4</span>
                    <input type="text" class="form-control" v-model="newQuestion.option4">
                    <span class="input-group-text">
                      <input class="form-check-input" type="radio" v-model="newQuestion.correct_option" value="4">
                    </span>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Add Question</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Edit Quiz Modal -->
      <div class="modal fade" id="editQuizModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Quiz</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="editQuiz">
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Quiz Title</label>
                  <input type="text" class="form-control" v-model="quiz.title" required>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Date</label>
                    <input type="date" class="form-control" v-model="quiz.date_of_quiz" required>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Duration (HH:MM)</label>
                    <input type="text" class="form-control" v-model="quiz.time_duration" required>
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label">Remarks</label>
                  <textarea class="form-control" v-model="quiz.remarks" rows="2"></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Edit Question Modals -->
      <div v-for="question in quiz.questions" :key="`edit-question-${question.id}`" class="modal fade"
        :id="`editQuestionModal${question.id}`" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Question</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="editQuestion(question)">
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Question Statement</label>
                  <textarea class="form-control" v-model="question.question_statement" rows="3" required></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Options</label>
                  <div class="input-group mb-2">
                    <span class="input-group-text">1</span>
                    <input type="text" class="form-control" v-model="question.option1" required>
                    <span class="input-group-text">
                      <input class="form-check-input" type="radio" v-model="question.correct_option" value="1">
                    </span>
                  </div>
                  <div class="input-group mb-2">
                    <span class="input-group-text">2</span>
                    <input type="text" class="form-control" v-model="question.option2" required>
                    <span class="input-group-text">
                      <input class="form-check-input" type="radio" v-model="question.correct_option" value="2">
                    </span>
                  </div>
                  <div class="input-group mb-2">
                    <span class="input-group-text">3</span>
                    <input type="text" class="form-control" v-model="question.option3">
                    <span class="input-group-text">
                      <input class="form-check-input" type="radio" v-model="question.correct_option" value="3">
                    </span>
                  </div>
                  <div class="input-group mb-2">
                    <span class="input-group-text">4</span>
                    <input type="text" class="form-control" v-model="question.option4">
                    <span class="input-group-text">
                      <input class="form-check-input" type="radio" v-model="question.correct_option" value="4">
                    </span>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Save Changes</button>
              </div>
            </form>
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
  name: 'Quiz',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const quiz = ref({ id: '', title: '', date_of_quiz: '', time_duration: '', remarks: '', chapter_id: '', chapter_name: '', subject_id: '', subject_name: '', questions: [] });
    const newQuestion = ref({ question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_option: '1' });

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
          const data = await response.json();
          // Ensure correct_option is treated as string for radio inputs
          data.questions = data.questions.map(q => ({
            ...q,
            correct_option: String(q.correct_option)
          }));
          quiz.value = data;
        } else {
          console.error('Failed to fetch quiz:', await response.json());
        }
      } catch (error) {
        console.error('Error fetching quiz:', error);
      }
    };

    const createQuestion = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${route.params.id}/questions`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newQuestion.value),
        });
        if (response.ok) {
          newQuestion.value = { question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_option: '1' };
          await fetchQuiz();
          window.bootstrap.Modal.getInstance(document.getElementById('createQuestionModal')).hide();
        } else {
          console.error('Failed to create question:', await response.json());
        }
      } catch (error) {
        console.error('Error creating question:', error);
      }
    };

    const editQuiz = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${route.params.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: quiz.value.title,
            date_of_quiz: quiz.value.date_of_quiz,
            time_duration: quiz.value.time_duration,
            remarks: quiz.value.remarks,
          }),
        });
        if (response.ok) {
          await fetchQuiz();
          window.bootstrap.Modal.getInstance(document.getElementById('editQuizModal')).hide();
        } else {
          console.error('Failed to edit quiz:', await response.json());
        }
      } catch (error) {
        console.error('Error editing quiz:', error);
      }
    };

    const editQuestion = async (question) => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/questions/${question.id}`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question_statement: question.question_statement,
            option1: question.option1,
            option2: question.option2,
            option3: question.option3,
            option4: question.option4,
            correct_option: parseInt(question.correct_option)
          }),
        });
        if (response.ok) {
          await fetchQuiz();
          window.bootstrap.Modal.getInstance(document.getElementById(`editQuestionModal${question.id}`)).hide();
        } else {
          console.error('Failed to edit question:', await response.json());
        }
      } catch (error) {
        console.error('Error editing question:', error);
      }
    };

    const deleteQuestion = async (questionId) => {
      if (confirm('Are you sure you want to delete this question?')) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/questions/${questionId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json',
            },
          });
          if (response.ok) {
            await fetchQuiz();
          } else {
            console.error('Failed to delete question:', await response.json());
          }
        } catch (error) {
          console.error('Error deleting question:', error);
        }
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
      newQuestion,
      createQuestion,
      editQuiz,
      editQuestion,
      deleteQuestion,
      logout,
    };
  },
};
</script>

<style scoped>
.question-item {
  border-left: 4px solid #36b9cc;
  background-color: #f8f9fa;
}

.correct-option {
  background-color: #d4edda;
  padding: 5px 10px;
  border-radius: 4px;
  display: inline-block;
}

.option {
  padding: 5px 10px;
  border-radius: 4px;
}
</style>