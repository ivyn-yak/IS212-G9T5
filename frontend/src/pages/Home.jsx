import React, { useEffect } from 'react';

function Home() {
  useEffect(() => {
    console.log('Home component rendered');
  }, []);

  return (
    <div>
      <h1>Hello, welcome to our page!</h1>
      <p>We are penultimate students from SMU Information Systems, and this is our Work From Home System application for Software Project Management (IS212).</p>
      <p>Here is a link to our <a href="https://github.com/nlcchi/IS212-G9T5">GitHub repository</a>!</p>
      <p>To navigate through the application, please use these Staff IDs to try out the different roles and access control:</p>
      <table>
        <thead>
          <tr>
            <th>Staff Role</th>
            <th>Staff ID</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Staff</td>
            <td><a href="https://is-212-g9-t5.vercel.app/140002">140002</a></td>
          </tr>
          <tr>
            <td>Manager</td>
            <td><a href="https://is-212-g9-t5.vercel.app/140894">140894</a></td>
          </tr>
          <tr>
            <td>HR</td>
            <td><a href="https://is-212-g9-t5.vercel.app/" aria-disabled></a>No IDs yet</td>
          </tr>
          <tr>
            <td>Senior Manager/Director</td>
            <td><a href="https://is-212-g9-t5.vercel.app/140001">140001</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Home;