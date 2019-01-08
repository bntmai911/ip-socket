import React from 'react';
import DefaultLayout from './containers/DefaultLayout';

const Dashboard = React.lazy(() => import('./views/Dashboard'));
const Users = React.lazy(() => import('./views/SocialWeb/Users'));
const UserDetail = React.lazy(() => import('./views/SocialWeb/UserDetail'));
const CreateBlog = React.lazy(() => import('./views/SocialWeb/CreateBlog'));
const Login = React.lazy(() => import('./views/SocialWeb/Login/Login'));
const Register = React.lazy(() => import('./views/SocialWeb/Register/Register'));

// https://github.com/ReactTraining/react-router/tree/master/packages/react-router-config
const routes = [
  { path: '/home', exact: true, name: 'Home', component: DefaultLayout },
  { path: '/home/login', exact: false, name: 'Home', component: Login },
  { path: '/home/register', exact: true, name: 'Home', component: Register },
  { path: '/home/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/home/users', exact: true,  name: 'Users', component: Users },
  { path: '/home/profile', exact: false, name: 'User Page', component: UserDetail },
  { path: '/home/create-blog', exact: true, name: 'User Page', component: CreateBlog },
];

export default routes;
