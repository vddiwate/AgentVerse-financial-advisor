"""Database seeding engine to load configurations and prompts from JSON into PostgreSQL."""

import os
import json
import sys
from pathlib import Path

# Append project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from agentverse_backend.db.database import SessionLocal
from agentverse_backend.db.models import AgentRegistry, ToolRegistry, PromptRegistry
from agentverse_backend.utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent

def seed_db():
    """Initializes tables and populates database with agents, tools, and prompts configuration from JSON."""
    logger.info("Initializing database session for seeding...")
    db = SessionLocal()
    
    try:
        # Load seed data from JSON configuration file
        seed_file_path = BASE_DIR / "seed_data.json"
        with open(seed_file_path, "r", encoding="utf-8") as f:
            seed_data = json.load(f)
            
        agents_added = 0
        agents_updated = 0
        agents_existing = 0
        logger.info("Seeding Agent Registry...")
        for agent_info in seed_data["agents"]:
            exists = db.query(AgentRegistry).filter(AgentRegistry.agent_name == agent_info["agent_name"]).first()
            if not exists:
                agent = AgentRegistry(
                    agent_name=agent_info["agent_name"],
                    description=agent_info["description"]
                )
                db.add(agent)
                agents_added += 1
            else:
                # Update description if it has changed in JSON config
                if exists.description != agent_info["description"]:
                    exists.description = agent_info["description"]
                    agents_updated += 1
                else:
                    agents_existing += 1
        # Commit agents first to generate primary key IDs
        db.commit()
        
        tools_added = 0
        tools_updated = 0
        tools_existing = 0
        logger.info("Seeding Tool Registry...")
        for tool_info in seed_data["tools"]:
            # Find associated agent to map foreign key
            agent = db.query(AgentRegistry).filter(AgentRegistry.agent_name == tool_info["agent_name"]).first()
            agent_id = agent.agent_id if agent else None
            
            exists = db.query(ToolRegistry).filter(ToolRegistry.tool_name == tool_info["tool_name"]).first()
            if not exists:
                tool = ToolRegistry(
                    tool_name=tool_info["tool_name"],
                    description=tool_info["description"],
                    agent_id=agent_id
                )
                db.add(tool)
                tools_added += 1
            else:
                # Sync tool details and mappings if they changed
                updated = False
                if exists.agent_id != agent_id:
                    exists.agent_id = agent_id
                    updated = True
                if exists.description != tool_info["description"]:
                    exists.description = tool_info["description"]
                    updated = True
                
                if updated:
                    tools_updated += 1
                else:
                    tools_existing += 1
                
        prompts_added = 0
        prompts_updated = 0
        prompts_existing = 0
        logger.info("Seeding Prompt Registry...")
        for prompt_info in seed_data["prompts"]:
            # Find associated agent to map foreign key
            agent = db.query(AgentRegistry).filter(AgentRegistry.agent_name == prompt_info["agent_name"]).first()
            agent_id = agent.agent_id if agent else None
            
            exists = db.query(PromptRegistry).filter(PromptRegistry.prompt_name == prompt_info["prompt_name"]).first()
            if not exists:
                prompt = PromptRegistry(
                    prompt_name=prompt_info["prompt_name"],
                    prompt_text=prompt_info["prompt_text"],
                    agent_id=agent_id
                )
                db.add(prompt)
                prompts_added += 1
            else:
                # Sync prompt text or parent agent mapping if they changed
                updated = False
                if exists.prompt_text != prompt_info["prompt_text"]:
                    exists.prompt_text = prompt_info["prompt_text"]
                    updated = True
                if exists.agent_id != agent_id:
                    exists.agent_id = agent_id
                    updated = True
                
                if updated:
                    prompts_updated += 1
                else:
                    prompts_existing += 1
                
        db.commit()
        logger.success("Database seeding completed successfully!")
        logger.info("Summary of changes:")
        logger.info(f"  - Agents:  {agents_added} added, {agents_updated} updated, {agents_existing} unchanged.")
        logger.info(f"  - Tools:   {tools_added} added, {tools_updated} updated, {tools_existing} unchanged.")
        logger.info(f"  - Prompts: {prompts_added} added, {prompts_updated} updated, {prompts_existing} unchanged.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error during seeding transaction: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
