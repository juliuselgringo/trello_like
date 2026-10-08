export function useProjectTasks(tasks) {
    // récupérer les tâches d'un projet spécifique
    const getProjectTasks = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id);
        return found ? found.length : 0;
    };

    // récupérer les tâches terminées d'un projet spécifique
    const getProjectTasksDone = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id && t.column === 3);
        return found ? found.length : 0;
    };

    // récupérer les tâches à faire d'un projet spécifique
    const getProjectTasksToDo = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id && t.column === 1);
        return found ? found.length : 0;
    };

    // récupérer les tâches en retard d'un projet spécifique
    const getProjectTasksOverdue = (project_id) => {
        const found = tasks.value.filter(t => t.project === project_id && t.column !== 3 && new Date(t.task_dead_line) < Date.now());
        return found ? found.length : 0;
    };

    return { getProjectTasks, getProjectTasksDone, getProjectTasksToDo, getProjectTasksOverdue }
}