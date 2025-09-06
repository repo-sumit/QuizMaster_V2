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
        <h1 class="h3 mb-0 text-gray-800">{{ subject.name }}</h1>
        <div>
          <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#editSubjectModal">
            <i class="fas fa-edit"></i> Edit Subject
          </button>
          <router-link to="/admin/dashboard" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to Dashboard
          </router-link>
        </div>
      </div>

      <div class="card shadow mb-4">
        <div class="card-header py-3 d-flex justify-content-between align-items-center">
          <h6 class="m-0 font-weight-bold text-primary">Subject Details</h6>
          <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#createChapterModal">
            <i class="fas fa-plus"></i> Add Chapter
          </button>
        </div>
        <div class="card-body">
          <p>{{ subject.description }}</p>
          <div class="mt-4">
            <h5 class="font-weight-bold">Chapters</h5>
            <div v-for="chapter in chapters" :key="chapter.id" class="card chapter-card mb-3">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <h6 class="font-weight-bold text-success">{{ chapter.name }}</h6>
                    <p class="mb-0">{{ chapter.description }}</p>
                  </div>
                  <div>
                    <router-link :to="`/admin/chapter/${chapter.id}`" class="btn btn-sm btn-success">
                      <i class="fas fa-eye"></i> View
                    </router-link>
                    <button class="btn btn-sm btn-info" data-bs-toggle="modal"
                      :data-bs-target="`#editChapterModal${chapter.id}`">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" @click="deleteChapter(chapter.id)">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Chapter Modal -->
      <div class="modal fade" id="createChapterModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add Chapter to {{ subject.name }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="createChapter">
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

      <!-- Edit Subject Modal -->
      <div class="modal fade" id="editSubjectModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Subject</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="editSubject">
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

      <!-- Edit Chapter Modals -->
      <div v-for="chapter in chapters" :key="`edit-chapter-${chapter.id}`" class="modal fade"
        :id="`editChapterModal${chapter.id}`" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Chapter</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form @submit.prevent="editChapter(chapter.id)">
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
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'Subject',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const subject = ref({ id: '', name: '', description: '' });
    const chapters = ref([]);
    const newChapter = ref({ name: '', description: '' });

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

    const fetchSubject = async () => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${route.params.id}`, {
          method: 'GET',
          headers,
        });
        if (response.ok) {
          const data = await response.json();
          subject.value = data || { id: '', name: '', description: '' };
          console.log(data)
          chapters.value = data.chapters || [];
        } else {
          console.error('Failed to fetch subject:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error fetching subject:', error);
      }
    };

    const createChapter = async () => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${route.params.id}/chapters`, {
          method: 'POST',
          headers,
          body: JSON.stringify({ ...newChapter.value, create_chapter: 1 }),
        });
        if (response.ok) {
          newChapter.value = { name: '', description: '' };
          await fetchSubject();
          window.bootstrap.Modal.getInstance(document.getElementById('createChapterModal')).hide();
        } else {
          console.error('Failed to create chapter:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error creating chapter:', error);
      }
    };

    const editSubject = async () => {
      const headers = getHeaders();
      if (!headers) return;

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/subjects/${route.params.id}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(subject.value),
        });
        if (response.ok) {
          await fetchSubject();
          window.bootstrap.Modal.getInstance(document.getElementById('editSubjectModal')).hide();
        } else {
          console.error('Failed to edit subject:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error editing subject:', error);
      }
    };

    const editChapter = async (chapterId) => {
      const headers = getHeaders();
      if (!headers) return;

      const chapter = chapters.value.find(c => c.id === chapterId);
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/chapters/${chapterId}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(chapter),
        });
        if (response.ok) {
          await fetchSubject();
          window.bootstrap.Modal.getInstance(document.getElementById(`editChapterModal${chapterId}`)).hide();
        } else {
          console.error('Failed to edit chapter:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error editing chapter:', error);
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
          await fetchSubject();
        } else {
          console.error('Failed to delete chapter:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error deleting chapter:', error);
      }
    };

    const logout = () => {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      router.push('/login');
    };

    // Initial fetch
    fetchSubject();

    return {
      subject,
      chapters,
      newChapter,
      createChapter,
      editSubject,
      editChapter,
      deleteChapter,
      logout,
    };
  },
};
</script>

<style scoped>
.admin-nav {
  background-color: #343a40 !important;
}

.chapter-card {
  border-left: 4px solid #1cc88a;
}

.quiz-card {
  border-left: 4px solid #f6c23e;
}
</style>