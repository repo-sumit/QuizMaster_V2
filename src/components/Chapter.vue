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
          <router-link :to="`/admin/subject/${chapter.subject_id}`" class="text-primary text-decoration-none">{{ chapter.subject_name
          }}</router-link> /
          {{ chapter.name }}
        </h1>
        <div>
          <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editChapterModal">
            <i class="fas fa-edit"></i> Edit Chapter
          </button>
          <router-link :to="`/admin/subject/${chapter.subject_id}`" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to Chapters
          </router-link>
        </div>
      </div>

      <div class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-success">Chapter Details</h6>
        </div>
        <div class="card-body">
          <p>{{ chapter.description }}</p>
          <div class="mt-4">
            <h5 class="font-weight-bold">Quizzes</h5>
            <div v-for="quiz in chapter.quizzes" :key="quiz.id" class="card quiz-card mb-3">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="font-weight-bold text-warning">{{ quiz.title }}</h6>
                    <small class="text-muted">
                      Date: {{ quiz.date_of_quiz }} | Duration: {{ quiz.time_duration }}
                    </small>
                    <p v-if="quiz.remarks" class="mt-2 mb-0"><small>{{ quiz.remarks }}</small></p>
                  </div>
                  <div>
                    <router-link :to="`/admin/quiz/${quiz.id}`" class="btn btn-sm btn-warning">
                      <i class="fas fa-eye"></i> View
                    </router-link>
                    <button class="btn btn-sm btn-info" data-bs-toggle="modal"
                      :data-bs-target="`#editQuizModal${quiz.id}`">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" @click="deleteQuiz(quiz.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <button class="btn btn-warning mt-2" data-bs-toggle="modal" data-bs-target="#createQuizModal">
              <i class="fas fa-plus"></i> Add Quiz
            </button>
          </div>
        </div>
      </div>

      <!-- Create Quiz Modal -->
      <div class="modal fade" id="createQuizModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add New Quiz</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="createQuiz">
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Quiz Title</label>
                  <input type="text" class="form-control" v-model="newQuiz.title" required>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Date</label>
                    <input type="date" class="form-control" v-model="newQuiz.date_of_quiz" required>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Duration (HH:MM)</label>
                    <input type="text" class="form-control" v-model="newQuiz.time_duration" placeholder="00:30"
                      required>
                  </div>
                </div>
                <div class="mb-3">
                  <label class="form-label">Remarks</label>
                  <textarea class="form-control" v-model="newQuiz.remarks" rows="2"></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Create Quiz</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Edit Chapter Modal -->
      <div class="modal fade" id="editChapterModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Chapter</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="editChapter">
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Chapter Name</label>
                  <input type="text" class="form-control" v-model="chapter.name" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea class="form-control" v-model="chapter.description" rows="3"></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Edit Quiz Modals -->
      <div v-for="quiz in chapter.quizzes" :key="`edit-quiz-${quiz.id}`" class="modal fade"
        :id="`editQuizModal${quiz.id}`" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Quiz</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="editQuiz(quiz.id)">
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
                <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save Changes</button>
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
  name: 'Chapter',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const chapter = ref({ id: '', name: '', description: '', subject_id: '', subject: { name: '' }, quizzes: [] });
    const newQuiz = ref({ title: '', date_of_quiz: '', time_duration: '', remarks: '' });

    // Helper function to get headers with token
    const getHeaders = () => {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found in localStorage');
        router.push('/login'); // Redirect to login if token is missing
        return null;
      }
      return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, // Ensure proper Bearer token format
      };
    };

    const fetchChapter = async () => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/chapters/${route.params.id}`, {
          method: 'GET',
          headers,
        });
        if (response.ok) {
          chapter.value = await response.json();
        } else {
          console.error('Failed to fetch chapter:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error fetching chapter:', error);
      }
    };

    const createQuiz = async () => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/chapters/${route.params.id}/quizzes`, {
          method: 'POST',
          headers,
          body: JSON.stringify({ ...newQuiz.value, create_quiz: 1 }),
        });
        if (response.ok) {
          newQuiz.value = { title: '', date_of_quiz: '', time_duration: '', remarks: '' };
          await fetchChapter();
          window.bootstrap.Modal.getInstance(document.getElementById('createQuizModal')).hide();
        } else {
          console.error('Failed to create quiz:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error creating quiz:', error);
      }
    };

    const editChapter = async () => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/chapters/${route.params.id}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify({ name: chapter.value.name, description: chapter.value.description }),
        });
        if (response.ok) {
          await fetchChapter();
          window.bootstrap.Modal.getInstance(document.getElementById('editChapterModal')).hide();
        } else {
          console.error('Failed to edit chapter:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error editing chapter:', error);
      }
    };

    const editQuiz = async (quizId) => {
      const headers = getHeaders();
      if (!headers) return;

      const quiz = chapter.value.quizzes.find(q => q.id === quizId);
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${quizId}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(quiz),
        });
        if (response.ok) {
          await fetchChapter();
          window.bootstrap.Modal.getInstance(document.getElementById(`editQuizModal${quizId}`)).hide();
        } else {
          console.error('Failed to edit quiz:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error editing quiz:', error);
      }
    };

    const deleteQuiz = async (quizId) => {
      if (!confirm('Are you sure you want to delete this quiz?')) return;

      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/quizzes/${quizId}`, {
          method: 'DELETE',
          headers,
        });
        if (response.ok) {
          await fetchChapter();
        } else {
          console.error('Failed to delete quiz:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error deleting quiz:', error);
      }
    };
    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };
    // Initial fetch
    fetchChapter();

    return {
      chapter,
      newQuiz,
      createQuiz,
      editChapter,
      editQuiz,
      deleteQuiz,
      logout
    };
  },
};
</script>

<style scoped>
.admin-nav {
  background-color: #343a40 !important;
}

.quiz-card {
  border-left: 4px solid #f6c23e;
}

.question-item {
  border-left: 4px solid #36b9cc;
}
</style>