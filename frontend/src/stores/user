import { defineStore } from 'pinia'
import axios from "axios"

export const useUserStore = defineStore('user', {
    state: () => ({ firstname: 'FirstName', lastname: 'LastName', email: 'someone@someplace.org', isAdmin: false, isLoggedIn: false, avatar: 'male_avatar.png', id: '', user_color: '', male: true, isChild: false }),
    getters: {
      fullname: (state) => state.firstname + ' ' + state.lastname,
      getID: (state) => state.id,
    },
    actions: {
      loginUser(firstname, lastname, email, isAdmin, male, id, user_color, groups) {
        this.firstname = firstname
        this.lastname = lastname
        this.email = email
        this.isAdmin = isAdmin
        this.isLoggedIn = true
        this.id = id
        this.user_color = user_color
        this.male = male
        
        if (groups.includes(1)){
          this.isChild = true
        } else {
          this.isChild = false
        }

        if (male) {
          if (this.isChild) {
            this.avatar = 'child_male_avatar.jpg'
          } else {
            this.avatar = 'adult_male_avatar.jpg';
          }
        } else {
          if (this.isChild) {
            this.avatar = 'child_female_avatar.jpg'
          } else {
            this.avatar = 'adult_female_avatar.jpg';
          }
        }
      },
      logoutUser() {
        this.firstname = 'FirstName'
        this.lastname = 'LastName'
        this.email = 'someone@somplace.org'
        this.isAdmin = false
        this.isLoggedIn = false
        this.avatar = 'male_avatar.jpg'
        this.id = ''
        this.user_color = ''
        this.male = true
      },
      async updateProfile(user) {
        try {
          // Make a POST request to your API endpoint
          const response = await axios.patch('https://chores.danielleandjohn.love/api/users/' + user.id + '/', user);

          // Add area to local storage
          //this.areas.push(area);
          this.loginUser(user.first_name, user.last_name, user.email, user.isAdmin, user.male, user.id, user.user_color);

        } catch (error) {
          // Handle errors (e.g., show an error message)
          console.log('Error:', error);
        }
      }, 
    },
    persist: true,
})