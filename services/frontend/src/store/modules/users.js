import axios from 'axios';

const state = {
    user: null,
};

const getters = {
    isAuthenticated: state => !!state.user,
    stateUser: state => state.user,
};

const actions = {
    async register({ dispatch }, form) {
        await axios.post('api/v1/user/register', form);
        await dispatch('logIn', form);
    },
    async logIn({ dispatch }, user) {
        await axios.post('api/v1/user/login/token', user);
        await dispatch('viewMe');
    },
    async viewMe({ commit }) {
        let { data } = await axios.get('api/v1/user/');
        console.log(data)
        await commit('setUser', data);
    },
    // async deleteUser({ }, id) {
    //     await axios.delete(`user/${id}`);
    // },
    async logOut({ commit }) {
        let user = null;
        commit('logout', user);
    }
};

const mutations = {
    setUser(state, username) {
        state.user = username;
    },
    logout(state, user) {
        state.user = user;
    },
};

export default {
    state,
    getters,
    actions,
    mutations
};
