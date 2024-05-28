from fastapi import FastAPI, HTTPException
import os
from ro_py.client import Client
from dotenv import load_dotenv
import logging
import asyncio

load_dotenv()

RobloxCookie = os.getenv("COOKIE")
APIKEY = os.getenv("API_KEY")

client = Client(RobloxCookie)
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/group/promote/")
async def promote_user(user_name: str, key: str, groupid: int):
    if key == APIKEY:
        try:
            group = await client.get_group(groupid)
            usernameinsystem = await client.get_user_by_username(user_name)
            if not usernameinsystem:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_id = usernameinsystem.id
            membertorank = await group.get_member_by_id(user_id)
            if not membertorank:
                raise HTTPException(status_code=404, detail="Member not found in group")
            
            await membertorank.promote()
            return {"message": "The user was promoted!"}
        except Exception as e:
            logger.error(f"Error promoting user: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        raise HTTPException(status_code=403, detail="Incorrect key")

@app.get("/group/demote/")
async def demote_user(user_name: str, key: str, groupid: int):
    if key == APIKEY:
        try:
            group = await client.get_group(groupid)
            usernameinsystem = await client.get_user_by_username(user_name)
            if not usernameinsystem:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_id = usernameinsystem.id
            membertorank = await group.get_member_by_id(user_id)
            if not membertorank:
                raise HTTPException(status_code=404, detail="Member not found in group")
            
            await membertorank.demote()
            return {"message": "The user was demoted!"}
        except Exception as e:
            logger.error(f"Error demoting user: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        raise HTTPException(status_code=403, detail="Incorrect key")

@app.get("/group/rank/")
async def rank_user(user_name: str, key: str, groupid: int, role_number: int):
    if key == APIKEY:
        try:
            group = await client.get_group(groupid)
            target = await group.get_member_by_username(user_name)
            if not target:
                raise HTTPException(status_code=404, detail="User not found in group")
            
            await target.setrole(role_number)
            return {"message": "The user had their rank changed"}
        except Exception as e:
            logger.error(f"Error ranking user: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        raise HTTPException(status_code=403, detail="Incorrect key")

@app.get("/group/members/")
async def group_members(key: str, groupid: int):
    if key == APIKEY:
        try:
            group = await client.get_group(groupid)
            return {"member_count": group.member_count}
        except Exception as e:
            logger.error(f"Error fetching group members: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    else:
        raise HTTPException(status_code=403, detail="Incorrect key")
