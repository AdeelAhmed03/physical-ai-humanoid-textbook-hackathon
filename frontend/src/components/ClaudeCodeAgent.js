import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import skillsManager from '../skills/SkillsManager';
import styles from './ClaudeCodeAgent.module.css';

const ClaudeCodeAgent = ({ chapterId, currentContent }) => {
  const { user, token } = useAuth();
  const [agentTask, setAgentTask] = useState('');
  const [agentResponse, setAgentResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedSkill, setSelectedSkill] = useState('');
  const [skillParams, setSkillParams] = useState({});

  const availableSkills = skillsManager.listSkills();

  const handleRunAgent = async () => {
    if (!agentTask.trim()) return;

    setLoading(true);
    setAgentResponse('');

    try {
      // Run the subagent task
      const result = await skillsManager.runSubagentTask(agentTask, {
        ...skillParams,
        token: token,
        chapterId: chapterId,
        currentContent: currentContent
      });

      setAgentResponse(JSON.stringify(result, null, 2));
    } catch (error) {
      setAgentResponse(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteSkill = async () => {
    if (!selectedSkill) return;

    setLoading(true);
    setAgentResponse('');

    try {
      const result = await skillsManager.executeSkill(
        selectedSkill,
        skillParams.method || 'default',
        ...skillParams.args || []
      );

      setAgentResponse(JSON.stringify(result, null, 2));
    } catch (error) {
      setAgentResponse(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className={styles.agentContainer}>
        <p className={styles.loginPrompt}>Please <a href="/auth">sign in</a> to use Claude Code Agent features.</p>
      </div>
    );
  }

  return (
    <div className={styles.agentContainer}>
      <h3>Claude Code Agent</h3>

      <div className={styles.agentControls}>
        <div className={styles.taskInput}>
          <label htmlFor="agentTask">Agent Task:</label>
          <textarea
            id="agentTask"
            value={agentTask}
            onChange={(e) => setAgentTask(e.target.value)}
            placeholder="Describe what you want the agent to do (e.g., 'Translate this chapter to Urdu', 'Personalize content based on my background')"
            rows="3"
          />
        </div>

        <div className={styles.skillSelector}>
          <label htmlFor="skillSelect">Or select a specific skill:</label>
          <select
            id="skillSelect"
            value={selectedSkill}
            onChange={(e) => setSelectedSkill(e.target.value)}
          >
            <option value="">Choose a skill...</option>
            {availableSkills.map(skill => (
              <option key={skill} value={skill}>{skill}</option>
            ))}
          </select>
        </div>

        <div className={styles.skillParams}>
          <label>Skill Parameters (JSON):</label>
          <textarea
            value={JSON.stringify(skillParams, null, 2)}
            onChange={(e) => {
              try {
                setSkillParams(JSON.parse(e.target.value));
              } catch (e) {
                // Ignore invalid JSON
              }
            }}
            placeholder="Enter parameters as JSON"
            rows="4"
          />
        </div>

        <div className={styles.buttonGroup}>
          <button
            onClick={handleRunAgent}
            disabled={loading || !agentTask.trim()}
            className={styles.agentButton}
          >
            {loading ? 'Running Agent...' : 'Run Agent Task'}
          </button>
          <button
            onClick={handleExecuteSkill}
            disabled={loading || !selectedSkill}
            className={styles.skillButton}
          >
            {loading ? 'Executing Skill...' : 'Execute Skill'}
          </button>
        </div>
      </div>

      {agentResponse && (
        <div className={styles.responseContainer}>
          <h4>Agent Response:</h4>
          <pre className={styles.responseContent}>{agentResponse}</pre>
        </div>
      )}

      <div className={styles.agentInfo}>
        <h4>Available Skills:</h4>
        <ul>
          {availableSkills.map(skill => (
            <li key={skill}>
              <strong>{skill}:</strong> {skillsManager.getSkillDescription(skill)}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ClaudeCodeAgent;