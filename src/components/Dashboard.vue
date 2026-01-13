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
      <div class="card glass-panel p-4 mb-4 bg-gradient-to-r from-sky-50 via-emerald-50 to-amber-50">
        <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
          <div>
            <span class="badge-soft">Admin workspace</span>
            <h1 class="h3 mb-1 display-font">Dashboard</h1>
            <p class="muted mb-0">Manage subjects, chapters, and keep your content organized.</p>
          </div>
          <div class="d-flex gap-2 ms-auto">
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createSubjectModal">
              <i class="fas fa-plus"></i> Add Subject
            </button>
            <button class="btn btn-primary" @click="exportData">
              <i class="fas fa-file-export"></i> Export
            </button>
            <button class="btn btn-outline-danger" @click="logout">
              <i class="fas fa-sign-out-alt"></i> Logout
            </button>
          </div>
        </div>
      </div>

      <div class="row g-4 mb-4">
        <div class="col-md-4">
          <div class="card stat-card h-100">
            <div class="card-body">
              <p class="muted small mb-1">Subjects</p>
              <div class="d-flex align-items-center justify-content-between">
                <h3 class="mb-0 display-font">{{ subjectCount }}</h3>
                <i class="fas fa-book fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card stat-card h-100">
            <div class="card-body">
              <p class="muted small mb-1">Chapters</p>
              <div class="d-flex align-items-center justify-content-between">
                <h3 class="mb-0 display-font">{{ chapterCount }}</h3>
                <i class="fas fa-folder fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card stat-card h-100">
            <div class="card-body">
              <p class="muted small mb-1">Quizzes</p>
              <div class="d-flex align-items-center justify-content-between">
                <h3 class="mb-0 display-font">{{ quizCount }}</h3>
                <i class="fas fa-question-circle fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card glass-panel p-3 mb-4">
        <div class="d-flex flex-wrap gap-3 align-items-center justify-content-between">
          <div class="flex-grow-1">
            <div class="input-group">
              <span class="input-group-text bg-white"><i class="fas fa-search"></i></span>
              <input v-model="subjectQuery" type="text" class="form-control" placeholder="Search subjects...">
            </div>
          </div>
          <div class="dropdown">
            <button class="btn btn-outline-brand dropdown-toggle" type="button" data-bs-toggle="dropdown">
              Sort: {{ sortLabel }}
            </button>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><button class="dropdown-item" @click="subjectSort = 'name_asc'">Name (A-Z)</button></li>
              <li><button class="dropdown-item" @click="subjectSort = 'name_desc'">Name (Z-A)</button></li>
              <li><button class="dropdown-item" @click="subjectSort = 'chapters_desc'">Most chapters</button></li>
              <li><button class="dropdown-item" @click="subjectSort = 'quizzes_desc'">Most quizzes</button></li>
            </ul>
          </div>
        </div>
      </div>

      <div class="row">
        <div v-for="subject in filteredSubjects" :key="subject.id" class="col-lg-6 mb-4">
          <div class="card subject-card shadow">
            <div class="card-header py-3 d-flex justify-content-between align-items-center">
              <h6 class="m-0 font-weight-bold text-primary">{{ subject.name }}</h6>
              <div>
                <button class="btn btn-sm btn-info" data-bs-toggle="modal"
                  :data-bs-target="`#editSubjectModal${subject.id}`">
                  <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteSubject(subject.id)">
                  <i class="fas fa-trash"></i>
                </button>
              </div>
            </div>
            <div class="card-body">
              <p>{{ subject.description }}</p>
              <div class="mt-3">
                <h6 class="font-weight-bold">Chapters</h6>
                <div v-for="chapter in subject.chapters" :key="chapter.id" class="card chapter-card mb-2">
                  <div class="card-body py-2">
                    <div class="d-flex justify-content-between align-items-center">
                      <router-link :to="`/admin/chapter/${chapter.id}`" class="text-success text-decoration-none">
                        {{ chapter.name }}
                      </router-link>
                      <div>
                        <!-- <button class="btn btn-sm btn-info" data-bs-toggle="modal"
                          :data-bs-target="`#editChapterModal${chapter.id}`">
                          <i class="fas fa-edit"></i>
                        </button> -->
                        <button class="btn btn-sm btn-danger" @click="deleteChapter(chapter.id)">
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                <button class="btn btn-sm btn-success mt-2" data-bs-toggle="modal"
                  :data-bs-target="`#createChapterModal${subject.id}`">
                  <i class="fas fa-plus"></i> Add Chapter
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Subject Modal -->
      <div class="modal fade" id="createSubjectModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Create New Subject</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="createSubject">
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Subject Name</label>
                  <input type="text" class="form-control" v-model="newSubject.name" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea class="form-control" v-model="newSubject.description" rows="3"></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Create Subject</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Edit Subject Modals -->
      <div v-for="subject in subjects" :key="`edit-${subject.id}`" class="modal fade"
        :id="`editSubjectModal${subject.id}`" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Subject</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="editSubject(subject.id)">
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Subject Name</label>
                  <input type="text" class="form-control" v-model="subject.name" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea class="form-control" v-model="subject.description" rows="3"></textarea>
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

      <!-- Create Chapter Modals -->
      <div v-for="subject in subjects" :key="`create-chapter-${subject.id}`" class="modal fade"
        :id="`createChapterModal${subject.id}`" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add Chapter to {{ subject.name }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="createChapter(subject.id)">
              <div class="modal-body">
                <div class="mb-3">
                  <label class="form-label">Chapter Name</label>
                  <input type="text" class="form-control" v-model="newChapter.name" required>
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea class="form-control" v-model="newChapter.description" rows="3"></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Add Chapter</button>
              </div>
            </form>
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
  name: 'Dashboard',
  setup() {
    const router = useRouter();
    const subjects = ref([]);
    const newSubject = ref({ name: '', description: '' });
    const newChapter = ref({ name: '', description: '' });
    const subjectQuery = ref('');
    const subjectSort = ref('name_asc');

    const subjectCount = computed(() => subjects.value.length);
    const chapterCount = computed(() => {
      return subjects.value.reduce((sum, subject) => sum + (subject.chapters ? subject.chapters.length : 0), 0);
    });
    const quizCount = computed(() => {
      return subjects.value.reduce((sum, subject) => {
        return sum + (subject.chapters || []).reduce((innerSum, chapter) => {
          return innerSum + (chapter.quizzes ? chapter.quizzes.length : 0);
        }, 0);
      }, 0);
    });

    const getQuizTotal = (subject) => {
      return (subject.chapters || []).reduce((sum, chapter) => {
        return sum + (chapter.quizzes ? chapter.quizzes.length : 0);
      }, 0);
    };

    const sortLabel = computed(() => {
      const labels = {
        name_asc: 'Name (A-Z)',
        name_desc: 'Name (Z-A)',
        chapters_desc: 'Most chapters',
        quizzes_desc: 'Most quizzes',
      };
      return labels[subjectSort.value] || 'Name (A-Z)';
    });

    const filteredSubjects = computed(() => {
      let list = [...subjects.value];
      const term = subjectQuery.value.trim().toLowerCase();
      if (term) {
        list = list.filter(subject =>
          subject.name.toLowerCase().includes(term) ||
          (subject.description || '').toLowerCase().includes(term)
        );
      }
      switch (subjectSort.value) {
        case 'name_desc':
          list.sort((a, b) => b.name.localeCompare(a.name));
          break;
        case 'chapters_desc':
          list.sort((a, b) => (b.chapters?.length || 0) - (a.chapters?.length || 0));
          break;
        case 'quizzes_desc':
          list.sort((a, b) => getQuizTotal(b) - getQuizTotal(a));
          break;
        default:
          list.sort((a, b) => a.name.localeCompare(b.name));
      }
      return list;
    });

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

    const fetchSubjects = async () => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/subjects', {
          method: 'GET',
          headers,
        });
        if (response.ok) {
          subjects.value = await response.json();
        } else {
          console.error('Failed to fetch subjects:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error fetching subjects:', error);
      }
    };

    const createSubject = async () => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch('http://127.0.0.1:5000/api/subjects', {
          method: 'POST',
          headers,
          body: JSON.stringify({ ...newSubject.value, create_subject: 1 }),
        });
        if (response.ok) {
          newSubject.value = { name: '', description: '' };
          await fetchSubjects();
          window.bootstrap.Modal.getInstance(document.getElementById('createSubjectModal')).hide();
        } else {
          console.error('Failed to create subject:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error creating subject:', error);
      }
    };

    const editSubject = async (subjectId) => {
      const headers = getHeaders();
      if (!headers) return;

      const subject = subjects.value.find(s => s.id === subjectId);
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${subjectId}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(subject),
        });
        if (response.ok) {
          await fetchSubjects();
          window.bootstrap.Modal.getInstance(document.getElementById(`editSubjectModal${subjectId}`)).hide();
        } else {
          console.error('Failed to edit subject:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error editing subject:', error);
      }
    };

    const deleteSubject = async (subjectId) => {
      if (!confirm('Are you sure you want to delete this subject?')) return;

      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${subjectId}`, {
          method: 'DELETE',
          headers,
        });
        if (response.ok) {
          await fetchSubjects();
        } else {
          console.error('Failed to delete subject:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error deleting subject:', error);
      }
    };

    const createChapter = async (subjectId) => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${subjectId}/chapters`, {
          method: 'POST',
          headers,
          body: JSON.stringify({ ...newChapter.value, create_chapter: 1 }),
        });
        if (response.ok) {
          newChapter.value = { name: '', description: '' };
          await fetchSubjects();
          window.bootstrap.Modal.getInstance(document.getElementById(`createChapterModal${subjectId}`)).hide();
        } else {
          console.error('Failed to create chapter:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error creating chapter:', error);
      }
    };

    const deleteChapter = async (chapterId) => {
      if (!confirm('Are you sure you want to delete this chapter?')) return;

      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/chapters/${chapterId}`, {
          method: 'DELETE',
          headers,
        });
        if (response.ok) {
          await fetchSubjects();
        } else {
          console.error('Failed to delete chapter:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error deleting chapter:', error);
      }
    };

    const exportData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/export', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          alert("Data export in progress. Please check your email.");
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'subjects_export.csv'; // Adjust filename as needed
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        } else {
          console.error('Failed to export data:', await response.json());
        }
      } catch (error) {
        console.error('Error exporting data:', error);
      }
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };
    // Initial fetch
    fetchSubjects();

    return {
      subjects,
      newSubject,
      newChapter,
      subjectCount,
      chapterCount,
      quizCount,
      subjectQuery,
      subjectSort,
      sortLabel,
      filteredSubjects,
      createSubject,
      editSubject,
      deleteSubject,
      createChapter,
      deleteChapter,
      exportData,
      logout
    };
  },
};
</script>

<style scoped>
.admin-nav {
  background-color: #ed1123 !important;
}

.admin-nav .navbar-brand,
.admin-nav .nav-link {
  color: rgba(241, 13, 13, 0.8) !important;
}

.subject-card {
  transition: all 0.3s ease;
  border-left: 4px solid #4e73df;
}

.chapter-card {
  border-left: 4px solid #1cc88a;
}

.quiz-card {
  border-left: 4px solid #f6c23e;
}

.question-item {
  border-left: 4px solid #36b9cc;
}

.score-card {
  border-left: 4px solid #4e73df;
}

.summary-card {
  border-left: 4px solid #1cc88a;
}
</style>
