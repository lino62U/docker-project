import React, { useState, useEffect } from 'react';
import Swal from 'sweetalert2';
import axios from 'axios';
import Header from './Header';
import Table from './Table';
import Add from './Add';
import Edit from './Edit';

const Dashboard = ({ setIsAuthenticated }) => {
  const [employees, setEmployees] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    // Obtener empleados desde el backend con Axios
    axios.get('http://127.0.0.1:5000/employees')
      .then(response => {
        if (Array.isArray(response.data)) {
          setEmployees(response.data);
        } else {
          console.error('Error fetching employees:', response.data);
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to load employees from server',
          });
        }
      })
      .catch(error => {
        console.error('Error fetching employees:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to connect to server',
        });
      });
  }, []);

  const handleEdit = id => {
    const [employee] = employees.filter(employee => employee.id === id);
    setSelectedEmployee(employee);
    setIsEditing(true);
  };

  const handleDelete = id => {
    Swal.fire({
      icon: 'warning',
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, cancel!',
    }).then(result => {
      if (result.isConfirmed) {
        axios.delete(`http://127.0.0.1:5000/employees/${id}`)
          .then(response => {
            if (response.data.error) {
              throw new Error(response.data.error);
            }
            Swal.fire({
              icon: 'success',
              title: 'Deleted!',
              text: response.data.message,
              showConfirmButton: false,
              timer: 1500,
            });
            // Actualizar la lista de empleados
            setEmployees(employees.filter(employee => employee.id !== id));
          })
          .catch(error => {
            console.error('Error deleting employee:', error);
            Swal.fire({
              icon: 'error',
              title: 'Error',
              text: 'Failed to delete employee',
            });
          });
      }
    });
  };

  return (
    <div className="container">
      {!isAdding && !isEditing && (
        <>
          <Header
            setIsAdding={setIsAdding}
            setIsAuthenticated={setIsAuthenticated}
          />
          <Table
            employees={employees}
            handleEdit={handleEdit}
            handleDelete={handleDelete}
          />
        </>
      )}
      {isAdding && (
        <Add
          employees={employees}
          setEmployees={setEmployees}
          setIsAdding={setIsAdding}
        />
      )}
      {isEditing && (
        <Edit
          employees={employees}
          selectedEmployee={selectedEmployee}
          setEmployees={setEmployees}
          setIsEditing={setIsEditing}
        />
      )}
    </div>
  );
};

export default Dashboard;