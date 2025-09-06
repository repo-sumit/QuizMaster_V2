<template>
      <router-view></router-view>
</template>

<script></script>

<style>
body {
  background-color: rgb(248, 248, 248);
}

.navbar-brand {
  font-weight: 700;
}

.card {
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.btn-primary {
  background-color: #4e73df;
  border-color: #4e73df;
}

.btn-primary:hover {
  background-color: #3a5ec0;
  border-color: #3a5ec0;
}

.footer {
  background-color: #f8f9fa;
  padding: 20px 0;
  margin-top: 50px;
}
</style>
