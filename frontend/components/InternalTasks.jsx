'use client';

import { useState, useEffect } from 'react';
import { internalTasksAPI } from '@/lib/api';
import styles from './InternalTasks.module.css';

export default function InternalTasks({ bookingId }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formError, setFormError] = useState(null);
  const [formSuccess, setFormSuccess] = useState(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [filter, setFilter] = useState('');

  // Fetch tasks
  useEffect(() => {
    fetchTasks();
  }, [bookingId, filter]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await internalTasksAPI.getTasks(bookingId, filter || null);
      setTasks(data);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError(`Failed to fetch tasks: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Handle form submission
  const handleCreateTask = async (e) => {
    e.preventDefault();
    setFormError(null);
    setFormSuccess(null);

    if (!title.trim()) {
      setFormError('Task title is required');
      return;
    }

    try {
      setIsSubmitting(true);
      await internalTasksAPI.createTask(bookingId, {
        title: title.trim(),
        description: description.trim() || null,
      });

      setFormSuccess('Task created successfully!');
      setTitle('');
      setDescription('');
      
      // Refetch tasks
      await fetchTasks();
    } catch (err) {
      console.error('Error creating task:', err);
      const errorMessage = err.response?.data?.detail || err.message;
      setFormError(`Failed to create task: ${errorMessage}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle status change
  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await internalTasksAPI.updateTaskStatus(taskId, newStatus);
      await fetchTasks();
      setFormSuccess('Task status updated successfully!');
      setTimeout(() => setFormSuccess(null), 3000);
    } catch (err) {
      console.error('Error updating task status:', err);
      setError(`Failed to update status: ${err.response?.data?.detail || err.message}`);
    }
  };

  // Handle task deletion
  const handleDeleteTask = async (taskId) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await internalTasksAPI.deleteTask(taskId);
      await fetchTasks();
      setFormSuccess('Task deleted successfully!');
      setTimeout(() => setFormSuccess(null), 3000);
    } catch (err) {
      console.error('Error deleting task:', err);
      setError(`Failed to delete task: ${err.response?.data?.detail || err.message}`);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      open: '#ff9800',
      in_progress: '#2196f3',
      resolved: '#4caf50',
      closed: '#9e9e9e',
    };
    return colors[status] || '#757575';
  };

  return (
    <div className={styles.container}>
      <h2>Internal Tasks for Booking {bookingId}</h2>

      {/* Error Message */}
      {error && (
        <div className={styles.errorMessage} role="alert">
          {error}
        </div>
      )}

      {/* Success Message */}
      {formSuccess && (
        <div className={styles.successMessage} role="alert">
          {formSuccess}
        </div>
      )}

      {/* Form to Create Task */}
      <div className={styles.formSection}>
        <h3>Create New Task</h3>
        {formError && (
          <div className={styles.formError} role="alert">
            {formError}
          </div>
        )}
        
        <form onSubmit={handleCreateTask} className={styles.form}>
          <div className={styles.formGroup}>
            <label htmlFor="title">Task Title *</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter task title"
              required
              maxLength="255"
              disabled={isSubmitting}
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter task description (optional)"
              maxLength="1000"
              rows="4"
              disabled={isSubmitting}
            />
          </div>

          <button type="submit" disabled={isSubmitting} className={styles.submitButton}>
            {isSubmitting ? 'Creating...' : 'Create Task'}
          </button>
        </form>
      </div>

      {/* Filter Section */}
      <div className={styles.filterSection}>
        <label htmlFor="status-filter">Filter by Status:</label>
        <select
          id="status-filter"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className={styles.filterSelect}
        >
          <option value="">All</option>
          <option value="open">Open</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </select>
      </div>

      {/* Tasks List */}
      <div className={styles.tasksSection}>
        <h3>Tasks List</h3>
        
        {loading ? (
          <div className={styles.loading}>Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div className={styles.noTasks}>
            {filter ? 'No tasks found with this filter.' : 'No tasks yet.'}
          </div>
        ) : (
          <div className={styles.tasksList}>
            {tasks.map((task) => (
              <div key={task.id} className={styles.taskCard}>
                <div className={styles.taskHeader}>
                  <h4>{task.title}</h4>
                  <span
                    className={styles.statusBadge}
                    style={{ backgroundColor: getStatusColor(task.status) }}
                  >
                    {task.status.replace('_', ' ')}
                  </span>
                </div>

                {task.description && (
                  <p className={styles.taskDescription}>{task.description}</p>
                )}

                <div className={styles.taskMeta}>
                  <small>
                    Created: {new Date(task.created_at).toLocaleString()}
                  </small>
                  <small>
                    Updated: {new Date(task.updated_at).toLocaleString()}
                  </small>
                </div>

                <div className={styles.taskActions}>
                  <select
                    value={task.status}
                    onChange={(e) => handleStatusChange(task.id, e.target.value)}
                    className={styles.statusSelect}
                  >
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                    <option value="closed">Closed</option>
                  </select>

                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className={styles.deleteButton}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
