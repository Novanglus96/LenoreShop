import { defineStore } from "pinia";

export const useItemStore = defineStore("item", {
  state: () => ({
    pageinfo: {
      page: 1,
      page_size: 10,
    },
  }),
  getters: {},
  actions: {},
});
