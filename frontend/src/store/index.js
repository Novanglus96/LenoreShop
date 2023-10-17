// stores/chore

import { createStore } from 'vuex';

export default createStore({
  state: {
    authToken: null, // Initial state for your auth token
    // Add other state variables as needed
  },
  mutations: {
    setAuthToken(state, token) {
      state.authToken = token;
    },
    clearAuthToken(state) {
      state.authToken = null;
    },
    // Define other mutations as needed
  },
  actions: {
    setAuthToken({ commit }, token) {
      commit('setAuthToken', token);
    },
    clearAuthToken({ commit }) {
      commit('clearAuthToken');
    },
    // Define other actions as needed
  },
  getters: {
    isAuthenticated(state) {
      return !!state.authToken;
    },
    // Define other getters as needed
  },
});
