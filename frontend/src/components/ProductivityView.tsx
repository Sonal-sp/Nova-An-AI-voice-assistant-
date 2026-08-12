import React, { useState, useEffect } from 'react';
import { Trash2, Check } from 'lucide-react';
import { fetchNotes, createNote, deleteNote, fetchTodos, createTodo, toggleTodo, deleteTodo, fetchAgenda } from '../services/api';

export const ProductivityView: React.FC = () => {
  const [activeSubTab, setActiveSubTab] = useState<'notes' | 'todos' | 'agenda'>('notes');
  const [notes, setNotes] = useState<any[]>([]);
  const [todos, setTodos] = useState<any[]>([]);
  const [agenda, setAgenda] = useState<any>(null);

  // Form states
  const [noteTitle, setNoteTitle] = useState('');
  const [noteContent, setNoteContent] = useState('');
  const [noteTags, setNoteTags] = useState('');

  const [todoTask, setTodoTask] = useState('');
  const [todoPriority, setTodoPriority] = useState('Medium');

  useEffect(() => {
    loadData();
  }, [activeSubTab]);

  const loadData = async () => {
    try {
      if (activeSubTab === 'notes') setNotes(await fetchNotes());
      if (activeSubTab === 'todos') setTodos(await fetchTodos());
      if (activeSubTab === 'agenda') setAgenda(await fetchAgenda());
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!noteTitle.trim()) return;
    await createNote(noteTitle, noteContent, noteTags);
    setNoteTitle('');
    setNoteContent('');
    setNoteTags('');
    loadData();
  };

  const handleDeleteNote = async (id: number) => {
    await deleteNote(id);
    loadData();
  };

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!todoTask.trim()) return;
    await createTodo(todoTask, '', todoPriority);
    setTodoTask('');
    loadData();
  };

  const handleToggleTodo = async (id: number) => {
    await toggleTodo(id);
    loadData();
  };

  const handleDeleteTodo = async (id: number) => {
    await deleteTodo(id);
    loadData();
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-bold nova-gradient-text">⚡ Productivity Suite</h2>
            <p className="text-xs text-slate-400">Manage Notes, Tasks, Agenda, and Reminders</p>
          </div>

          <div className="flex items-center gap-2 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveSubTab('notes')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeSubTab === 'notes' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              📋 Notes
            </button>
            <button
              onClick={() => setActiveSubTab('todos')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeSubTab === 'todos' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              ✅ Checklist
            </button>
            <button
              onClick={() => setActiveSubTab('agenda')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeSubTab === 'agenda' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              📅 Daily Agenda
            </button>
          </div>
        </div>

        {/* Notes Tab */}
        {activeSubTab === 'notes' && (
          <div className="space-y-6">
            <form onSubmit={handleAddNote} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3">
              <input
                type="text"
                value={noteTitle}
                onChange={(e) => setNoteTitle(e.target.value)}
                placeholder="Note Title (e.g. Architecture Spec)..."
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
              />
              <textarea
                value={noteContent}
                onChange={(e) => setNoteContent(e.target.value)}
                placeholder="Note Content..."
                rows={2}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-sky-500"
              />
              <div className="flex items-center gap-3">
                <input
                  type="text"
                  value={noteTags}
                  onChange={(e) => setNoteTags(e.target.value)}
                  placeholder="Tags (work, nova)..."
                  className="flex-1 bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none"
                />
                <button type="submit" className="px-4 py-1.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-white text-xs font-bold transition-colors">
                  Save Note
                </button>
              </div>
            </form>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {notes.map((note) => (
                <div key={note.id} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xs font-bold text-sky-300">{note.title}</h4>
                    <button onClick={() => handleDeleteNote(note.id)} className="text-slate-500 hover:text-rose-400">
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                  <p className="text-xs text-slate-300 whitespace-pre-wrap">{note.content}</p>
                  {note.tags && <span className="text-[10px] font-mono text-slate-500">🏷️ {note.tags}</span>}
                </div>
              ))}
              {notes.length === 0 && <div className="col-span-2 text-center py-6 text-xs text-slate-500">No notes created yet.</div>}
            </div>
          </div>
        )}

        {/* Checklist Tab */}
        {activeSubTab === 'todos' && (
          <div className="space-y-6">
            <form onSubmit={handleAddTodo} className="flex items-center gap-3 p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <input
                type="text"
                value={todoTask}
                onChange={(e) => setTodoTask(e.target.value)}
                placeholder="New Task Description..."
                className="flex-1 bg-transparent border-none px-2 text-xs text-slate-100 placeholder-slate-500 focus:outline-none"
              />
              <select
                value={todoPriority}
                onChange={(e) => setTodoPriority(e.target.value)}
                className="bg-slate-950 border border-slate-800 rounded-lg px-2.5 py-1 text-xs text-slate-200"
              >
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
              <button type="submit" className="px-4 py-1.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-white text-xs font-bold transition-colors">
                Add Task
              </button>
            </form>

            <div className="space-y-2">
              {todos.map((todo) => {
                const isCompleted = todo.status === 'completed';
                return (
                  <div key={todo.id} className="flex items-center justify-between p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => handleToggleTodo(todo.id)}
                        className={`w-4 h-4 rounded border flex items-center justify-center ${
                          isCompleted ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-slate-600'
                        }`}
                      >
                        {isCompleted && <Check className="w-3 h-3" />}
                      </button>
                      <span className={`text-xs ${isCompleted ? 'line-through text-slate-500' : 'text-slate-200'}`}>
                        {todo.task}
                      </span>
                    </div>

                    <div className="flex items-center gap-3">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          todo.priority === 'High' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'
                        }`}
                      >
                        {todo.priority}
                      </span>
                      <button onClick={() => handleDeleteTodo(todo.id)} className="text-slate-500 hover:text-rose-400">
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                );
              })}
              {todos.length === 0 && <div className="text-center py-6 text-xs text-slate-500">No tasks in checklist.</div>}
            </div>
          </div>
        )}

        {/* Agenda Tab */}
        {activeSubTab === 'agenda' && (
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <h3 className="text-xs font-bold text-sky-400 mb-3">📅 Today's Aggregated Daily Agenda</h3>
            <div className="text-xs text-slate-300 leading-relaxed font-mono whitespace-pre-wrap">
              {agenda?.summary_markdown || 'No agenda items scheduled for today.'}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
