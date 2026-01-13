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
      <div class="card glass-panel p-4 mb-4 bg-gradient-to-r from-amber-50 via-orange-50 to-emerald-50">
        <div class="d-flex flex-wrap align-items-center justify-content-between gap-3">
          <div>
            <span class="badge-soft">Welcome back</span>
            <h1 class="h3 mb-1 display-font">Hello, {{ user.full_name }}</h1>
            <p class="muted mb-0">Track your wins, explore new subjects, and keep your momentum.</p>
          </div>
          <div class="d-flex flex-wrap align-items-center gap-2">
            <form class="d-inline" @submit.prevent="search">
              <div class="input-group">
                <input type="text" class="form-control" v-model="query" placeholder="Search subjects, chapters, quizzes">
                <button class="btn btn-primary" type="submit">
                  <i class="fas fa-search"></i>
                </button>
              </div>
            </form>
            <button class="btn btn-outline-danger" @click="logout">
              <i class="fas fa-sign-out-alt"></i>
              Logout
            </button>
          </div>
        </div>
      </div>

      <div class="row g-4 mb-4">
        <div class="col-xl-6">
          <div class="card border-left-primary h-100 py-2 stat-card">
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
        <div class="col-xl-6">
          <div class="card border-left-success h-100 py-2 stat-card">
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

      <div class="row g-4 mb-4">
        <div class="col-xl-6">
          <div class="card glass-panel p-3 h-100">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <div>
                <h5 class="mb-1 display-font">Subject Coverage</h5>
                <p class="muted small mb-0">See how content is distributed across subjects.</p>
              </div>
              <span class="score-chip">{{ subjects.length }} subjects</span>
            </div>
            <canvas ref="subjectChart"></canvas>
          </div>
        </div>
        <div class="col-xl-6">
          <div class="card glass-panel p-3 h-100">
            <div class="d-flex align-items-center justify-content-between mb-3">
              <div>
                <h5 class="mb-1 display-font">Score Pulse</h5>
                <p class="muted small mb-0">Your average score, visualized.</p>
              </div>
              <span class="badge-soft">Goal 85%</span>
            </div>
            <canvas ref="scoreChart"></canvas>
          </div>
        </div>
      </div>

      <div class="row g-4 mb-4">
        <div class="col-lg-6">
          <div class="card glass-panel p-4 h-100">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <h5 class="mb-0 display-font">Focus Sprint</h5>
              <span class="badge-soft">25 min</span>
            </div>
            <p class="muted small">Start a timed session to stay sharp while you study.</p>
            <div class="display-6 mb-3">{{ formattedTime }}</div>
            <div class="d-flex gap-2">
              <button class="btn btn-primary" @click="toggleTimer">
                <i class="fas" :class="timerRunning ? 'fa-pause' : 'fa-play'"></i>
                {{ timerRunning ? 'Pause' : 'Start' }}
              </button>
              <button class="btn btn-outline-brand" @click="resetTimer">
                <i class="fas fa-rotate-left"></i> Reset
              </button>
              <button class="btn btn-outline-brand" @click="toggleAmbient">
                <i class="fas" :class="ambientOn ? 'fa-volume-high' : 'fa-volume-xmark'"></i>
                {{ ambientOn ? 'Sound On' : 'Sound Off' }}
              </button>
            </div>
            <div class="progress mt-3" style="height: 10px;">
              <div class="progress-bar bg-success" role="progressbar" :style="{ width: `${timerProgress}%` }"></div>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card glass-panel p-4 h-100">
            <div class="d-flex align-items-center justify-content-between mb-2">
              <h5 class="mb-0 display-font">Quick Notes</h5>
              <span class="badge-soft">Auto-saved</span>
            </div>
            <p class="muted small">Jot down ideas or reminders while you browse quizzes.</p>
            <textarea class="form-control" rows="6" v-model="notes" @input="saveNotes"
              @keydown="handleNotesKeydown" placeholder="- Add bullet notes"></textarea>
          </div>
        </div>
      </div>

      <div class="row g-4 mb-4">
        <div class="col-lg-12">
          <div class="card glass-panel p-4 h-100">
            <div class="d-flex flex-wrap align-items-center justify-content-between gap-3 mb-2">
              <div>
                <h5 class="mb-0 display-font">Practice Mix</h5>
                <p class="muted small mb-0">Generate a quick mix of quizzes to test yourself.</p>
              </div>
              <div class="d-flex align-items-center gap-2">
                <select class="form-select" style="width: 140px;" v-model.number="mixSize">
                  <option :value="3">3 quizzes</option>
                  <option :value="5">5 quizzes</option>
                  <option :value="7">7 quizzes</option>
                </select>
                <button class="btn btn-outline-brand" @click="generatePracticeMix">
                  <i class="fas fa-shuffle"></i> Shuffle
                </button>
              </div>
            </div>
            <div v-if="practiceMix.length" class="row g-3">
              <div v-for="quiz in practiceMix" :key="quiz.id" class="col-md-4">
                <div class="card h-100 hover-lift">
                  <div class="card-body">
                    <p class="muted small mb-1">{{ quiz.subject }} / {{ quiz.chapter }}</p>
                    <h6 class="mb-2">{{ quiz.title }}</h6>
                    <router-link :to="`/user/quiz/${quiz.id}`" class="btn btn-primary btn-sm">
                      Start Quiz
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="muted small">No quizzes available yet.</div>
          </div>
        </div>
      </div>

      <div v-if="query" class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">Search Results for "{{ query }}"</h6>
        </div>
        <div class="card-body">
          <div v-if="filteredResults.subjects.length || filteredResults.chapters.length || filteredResults.quizzes.length">
            <div v-if="filteredResults.subjects.length">
              <h5>Subjects</h5>
              <div class="row">
                <div v-for="subject in filteredResults.subjects" :key="subject.id" class="col-lg-4 mb-4">
                  <div class="card h-100 hover-lift">
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
      <div v-else class="card shadow mb-4">
        <div class="card-header py-3 d-flex flex-wrap align-items-center justify-content-between gap-2">
          <h6 class="m-0 font-weight-bold text-primary">Available Subjects</h6>
          <div class="d-flex align-items-center gap-2">
            <div class="dropdown">
              <button class="btn btn-outline-brand dropdown-toggle btn-sm" type="button" data-bs-toggle="dropdown">
                Sort: {{ subjectSortLabel }}
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><button class="dropdown-item" @click="subjectSort = 'name_asc'">Name (A-Z)</button></li>
                <li><button class="dropdown-item" @click="subjectSort = 'name_desc'">Name (Z-A)</button></li>
                <li><button class="dropdown-item" @click="subjectSort = 'chapters_desc'">Most chapters</button></li>
                <li><button class="dropdown-item" @click="subjectSort = 'quizzes_desc'">Most quizzes</button></li>
              </ul>
            </div>
            <div class="dropdown">
              <button class="btn btn-outline-brand dropdown-toggle btn-sm" type="button" data-bs-toggle="dropdown">
                Filter: {{ subjectFilterLabel }}
              </button>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><button class="dropdown-item" @click="subjectFilter = 'all'">All subjects</button></li>
                <li><button class="dropdown-item" @click="subjectFilter = 'with_quizzes'">With quizzes</button></li>
                <li><button class="dropdown-item" @click="subjectFilter = 'with_chapters'">With chapters</button></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div class="row">
            <div v-for="subject in displayedSubjects" :key="subject.id" class="col-lg-4 mb-4">
              <div class="card h-100 hover-lift">
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
import { ref, computed, onMounted, watch, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'UserDashboard',
  setup() {
    const router = useRouter();
    const user = ref({ full_name: '' });
    const total_attempts = ref(0);
    const avg_score = ref(0);
    const query = ref('');
    const subjects = ref([]);
    const subjectSort = ref('name_asc');
    const subjectFilter = ref('all');
    const mixSize = ref(3);
    const practiceMix = ref([]);
    const subjectChart = ref(null);
    const scoreChart = ref(null);
    const notes = ref(localStorage.getItem('quizmaster_notes') || '');
    const timerSeconds = ref(1500);
    const timerRunning = ref(false);
    const ambientOn = ref(false);
    let audioContext = null;
    let ambientNodes = [];
    let timerInterval = null;
    let subjectChartInstance = null;
    let scoreChartInstance = null;

    const formattedTime = computed(() => {
      const minutes = Math.floor(timerSeconds.value / 60).toString().padStart(2, '0');
      const seconds = (timerSeconds.value % 60).toString().padStart(2, '0');
      return `${minutes}:${seconds}`;
    });

    const timerProgress = computed(() => {
      const total = 1500;
      return Math.min(100, Math.max(0, ((total - timerSeconds.value) / total) * 100));
    });

    const subjectSortLabel = computed(() => {
      const labels = {
        name_asc: 'Name (A-Z)',
        name_desc: 'Name (Z-A)',
        chapters_desc: 'Most chapters',
        quizzes_desc: 'Most quizzes',
      };
      return labels[subjectSort.value] || 'Name (A-Z)';
    });

    const subjectFilterLabel = computed(() => {
      const labels = {
        all: 'All subjects',
        with_quizzes: 'With quizzes',
        with_chapters: 'With chapters',
      };
      return labels[subjectFilter.value] || 'All subjects';
    });

    const getQuizTotal = (subject) => {
      return (subject.chapters || []).reduce((sum, chapter) => {
        return sum + (chapter.quizzes ? chapter.quizzes.length : 0);
      }, 0);
    };

    const displayedSubjects = computed(() => {
      let list = [...subjects.value];
      if (subjectFilter.value === 'with_quizzes') {
        list = list.filter(subject => getQuizTotal(subject) > 0);
      } else if (subjectFilter.value === 'with_chapters') {
        list = list.filter(subject => (subject.chapters || []).length > 0);
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

    const allQuizzes = computed(() => {
      const quizzes = [];
      subjects.value.forEach(subject => {
        (subject.chapters || []).forEach(chapter => {
          (chapter.quizzes || []).forEach(quiz => {
            quizzes.push({
              id: quiz.id,
              title: quiz.title,
              chapter: chapter.name,
              subject: subject.name,
            });
          });
        });
      });
      return quizzes;
    });

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
          generatePracticeMix();
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

    const search = () => {
      return;
    };

    const truncate = (text, length) => {
      if (!text || text.length <= length) return text;
      return text.substring(0, length) + '...';
    };

    const saveNotes = () => {
      notes.value = normalizeNotes(notes.value);
      localStorage.setItem('quizmaster_notes', notes.value);
    };

    const normalizeNotes = (value) => {
      if (!value) {
        return '- ';
      }
      const lines = value.split('\n').map(line => {
        if (!line.trim()) return '- ';
        return line.trim().startsWith('-') ? line.trim() : `- ${line.trim()}`;
      });
      return lines.join('\n');
    };

    const handleNotesKeydown = (event) => {
      if (event.key !== 'Enter') return;
      event.preventDefault();
      const textarea = event.target;
      const { selectionStart, selectionEnd } = textarea;
      const before = notes.value.substring(0, selectionStart);
      const after = notes.value.substring(selectionEnd);
      const insert = '\n- ';
      notes.value = `${before}${insert}${after}`;
      saveNotes();
      requestAnimationFrame(() => {
        const cursor = selectionStart + insert.length;
        textarea.selectionStart = cursor;
        textarea.selectionEnd = cursor;
      });
    };

    const startAmbient = () => {
      if (audioContext) return;
      const Context = window.AudioContext || window.webkitAudioContext;
      audioContext = new Context();

      const baseFrequencies = [110, 164.81, 220];
      ambientNodes = baseFrequencies.map(freq => {
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        gain.gain.value = 0.03;
        osc.connect(gain).connect(audioContext.destination);
        osc.start();
        return { osc, gain };
      });
    };

    const stopAmbient = () => {
      ambientNodes.forEach(node => {
        node.osc.stop();
      });
      ambientNodes = [];
      if (audioContext) {
        audioContext.close();
        audioContext = null;
      }
    };

    const toggleAmbient = () => {
      if (ambientOn.value) {
        ambientOn.value = false;
        stopAmbient();
        return;
      }
      ambientOn.value = true;
      startAmbient();
    };

    const generatePracticeMix = () => {
      const source = [...allQuizzes.value];
      if (!source.length) {
        practiceMix.value = [];
        return;
      }
      const mix = [];
      while (source.length && mix.length < mixSize.value) {
        const index = Math.floor(Math.random() * source.length);
        mix.push(source.splice(index, 1)[0]);
      }
      practiceMix.value = mix;
    };

    const toggleTimer = () => {
      if (timerRunning.value) {
        clearInterval(timerInterval);
        timerInterval = null;
        timerRunning.value = false;
        return;
      }
      timerRunning.value = true;
      timerInterval = setInterval(() => {
        if (timerSeconds.value > 0) {
          timerSeconds.value -= 1;
        } else {
          clearInterval(timerInterval);
          timerInterval = null;
          timerRunning.value = false;
        }
      }, 1000);
    };

    const resetTimer = () => {
      clearInterval(timerInterval);
      timerInterval = null;
      timerRunning.value = false;
      timerSeconds.value = 1500;
    };

    const buildSubjectChart = () => {
      if (!subjectChart.value) return;
      if (subjectChartInstance) {
        subjectChartInstance.destroy();
      }
      const labels = subjects.value.map(subject => subject.name);
      const data = subjects.value.map(subject =>
        (subject.chapters || []).reduce((sum, chapter) => sum + (chapter.quizzes ? chapter.quizzes.length : 0), 0)
      );
      subjectChartInstance = new Chart(subjectChart.value, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Quizzes',
              data,
              backgroundColor: '#38bdf8',
              borderRadius: 12,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true } },
        },
      });
    };

    const buildScoreChart = () => {
      if (!scoreChart.value) return;
      if (scoreChartInstance) {
        scoreChartInstance.destroy();
      }
      const scoreValue = Number(avg_score.value) || 0;
      scoreChartInstance = new Chart(scoreChart.value, {
        type: 'doughnut',
        data: {
          labels: ['Average Score', 'Remaining'],
          datasets: [
            {
              data: [scoreValue, Math.max(0, 100 - scoreValue)],
              backgroundColor: ['#0ea5a4', '#e2e8f0'],
              borderWidth: 0,
            },
          ],
        },
        options: {
          cutout: '70%',
          plugins: { legend: { display: false } },
        },
      });
    };

    watch([subjects, avg_score], () => {
      buildSubjectChart();
      buildScoreChart();
    }, { deep: true });

    onMounted(() => {
      notes.value = normalizeNotes(notes.value);
      fetchUserData();
      fetchSubjects();
    });

    onBeforeUnmount(() => {
      clearInterval(timerInterval);
      stopAmbient();
      if (subjectChartInstance) {
        subjectChartInstance.destroy();
      }
      if (scoreChartInstance) {
        scoreChartInstance.destroy();
      }
    });

    return {
      user,
      total_attempts,
      avg_score,
      query,
      subjects,
      filteredResults,
      logout,
      search,
      truncate,
      subjectChart,
      scoreChart,
      notes,
      saveNotes,
      handleNotesKeydown,
      timerRunning,
      formattedTime,
      timerProgress,
      toggleTimer,
      resetTimer,
      ambientOn,
      toggleAmbient,
      subjectSort,
      subjectFilter,
      subjectSortLabel,
      subjectFilterLabel,
      displayedSubjects,
      mixSize,
      practiceMix,
      generatePracticeMix,
    };
  },
};
</script>

<style scoped>
/* Styles inherited from App.vue */
</style>
