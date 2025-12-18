import { TextbookContentSkill, ChapterPersonalizationSkill, TranslationSkill } from './index';

class SkillsManager {
  constructor() {
    this.skills = new Map();
    this.initializeSkills();
  }

  initializeSkills() {
    // Register all available skills
    const textbookContentSkill = new TextbookContentSkill();
    const chapterPersonalizationSkill = new ChapterPersonalizationSkill();
    const translationSkill = new TranslationSkill();

    this.skills.set(textbookContentSkill.name, textbookContentSkill);
    this.skills.set(chapterPersonalizationSkill.name, chapterPersonalizationSkill);
    this.skills.set(translationSkill.name, translationSkill);

    console.log(`Skills Manager initialized with ${this.skills.size} skills:`,
                Array.from(this.skills.keys()).join(', '));
  }

  getSkill(skillName) {
    return this.skills.get(skillName);
  }

  async executeSkill(skillName, method, ...args) {
    const skill = this.getSkill(skillName);
    if (!skill) {
      throw new Error(`Skill '${skillName}' not found`);
    }

    if (typeof skill[method] !== 'function') {
      throw new Error(`Method '${method}' not found in skill '${skillName}'`);
    }

    try {
      return await skill[method](...args);
    } catch (error) {
      console.error(`Error executing skill ${skillName}.${method}:`, error);
      throw error;
    }
  }

  listSkills() {
    return Array.from(this.skills.keys());
  }

  getSkillDescription(skillName) {
    const skill = this.getSkill(skillName);
    return skill ? skill.description : null;
  }

  // Claude Code Subagent functionality
  async createSubagent(taskDescription, availableSkills = null) {
    // Create a specialized subagent that can use specific skills to accomplish a task
    const skillsToUse = availableSkills || this.listSkills();
    const skillInstances = skillsToUse.map(skillName => this.getSkill(skillName));

    return {
      id: `subagent_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      task: taskDescription,
      capabilities: skillsToUse,
      execute: async (params) => {
        // This would implement the subagent logic to accomplish the task
        // For now, we'll return a mock implementation
        console.log(`Subagent executing task: ${taskDescription}`, params);

        // Example: if the task involves translation, use the translation skill
        if (taskDescription.toLowerCase().includes('translate')) {
          const translationSkill = this.getSkill('translation');
          if (translationSkill && params.text && params.targetLanguage) {
            return await translationSkill.translateText(params.text, params.targetLanguage, params.token);
          }
        }

        // Example: if the task involves personalization, use the personalization skill
        if (taskDescription.toLowerCase().includes('personalize')) {
          const personalizationSkill = this.getSkill('chapter-personalization');
          if (personalizationSkill && params.chapterId) {
            return await personalizationSkill.getPersonalizedContent(
              params.chapterId,
              params.userBackground,
              params.preferences
            );
          }
        }

        // Default: return a message indicating the subagent was created
        return {
          status: 'completed',
          task: taskDescription,
          params: params,
          subagentId: this.id
        };
      }
    };
  }

  async runSubagentTask(taskDescription, params) {
    // Create and run a subagent for the specific task
    const subagent = await this.createSubagent(taskDescription);
    return await subagent.execute(params);
  }
}

// Create a singleton instance of the SkillsManager
const skillsManager = new SkillsManager();
export default skillsManager;