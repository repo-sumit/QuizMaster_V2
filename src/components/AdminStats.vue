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
        <h1 class="h3 mb-0 text-gray-800">Statistics</h1>
        <div class="d-flex gap-2 ms-auto">
          <button class="btn btn-primary" @click="exportData">
            <i class="fas fa-file-export"></i> Export
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row">
        <div class="col-xl-2 col-md-6 mb-4">
          <div class="card border-left-primary shadow h-100 py-2">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Subjects</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.subjects_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-book fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-2 col-md-6 mb-4">
          <div class="card border-left-success shadow h-100 py-2">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Chapters</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.chapters_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-folder fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-2 col-md-6 mb-4">
          <div class="card border-left-info shadow h-100 py-2">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Quizzes</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.quizzes_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-question-circle fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-2 col-md-6 mb-4">
          <div class="card border-left-warning shadow h-100 py-2">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Questions</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.questions_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-list fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-xl-2 col-md-6 mb-4">
          <div class="card border-left-danger shadow h-100 py-2">
            <div class="card-body">
              <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                  <div class="text-xs font-weight-bold text-danger text-uppercase mb-1">Users</div>
                  <div class="h5 mb-0 font-weight-bold text-gray-800">{{ stats.users_count }}</div>
                </div>
                <div class="col-auto">
                  <i class="fas fa-users fa-2x text-gray-300"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Score Summary Table -->
      <div class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">User Score Summary</h6>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Full Name</th>
                  <th>Total Attempts</th>
                  <th>Average Score (%)</th>
                </tr>
              </thead>
              <tbody>
                <!-- {{ score_summary }} -->
                <tr v-for="summary in score_summary" :key="summary.username">
                  <td>
                    <router-link :to="`/admin/user/${summary.user_id}/scores`" class="text-primary">{{
                      summary.username }}</router-link>
                  </td>
                  <td>{{ summary.full_name }}</td>
                  <td>{{ summary.total_attempts }}</td>
                  <td>{{ summary.avg_score }}</td>
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
  name: 'AdminStats',
  setup() {
    const router = useRouter();
    const stats = ref({ subjects_count: 0, chapters_count: 0, quizzes_count: 0, questions_count: 0, users_count: 0 });
    const score_summary = ref([]);
    const subjects = ref([]);

    const fetchDashboardData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/dashboard/admin', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
        });
        if (response.ok) {
          const data = await response.json();
          stats.value = data.stats;
          score_summary.value = data.score_summary.map(summary => ({
            ...summary,
            user_id: data.score_summary.find(s => s.username === summary.username)?.user_id || null
          }));
          subjects.value = data.subjects;
        } else {
          console.error('Failed to fetch dashboard data:', await response.json());
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
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
          a.download = 'subjects_export.csv';
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

    fetchDashboardData();

    return {
      stats,
      score_summary,
      subjects,
      exportData,
      logout,
    };
  },
};
</script>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}

.border-left-primary {
  border-left: 0.25rem solid #4e73df !important;
}

.border-left-success {
  border-left: 0.25rem solid #1cc88a !important;
}

.border-left-info {
  border-left: 0.25rem solid #36b9cc !important;
}

.border-left-warning {
  border-left: 0.25rem solid #f6c23e !important;
}

.border-left-danger {
  border-left: 0.25rem solid #e74a3b !important;
}
</style>