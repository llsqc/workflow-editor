import request from "@/pages/api/config"

/**
 * @description agent 基础接口
 */
interface AgentBase {
    id: string
    name: string
    description: string
    avatar: string
    kind: number
}

/**
 * @description Analyser agent (kind = 0)
 */
export interface AnalyseAgent extends AgentBase {
    identity_setting: string
    task: string
}

/**
 * @description Judge agent (kind = 1)
 */
export interface JudgeAgent extends AgentBase {
    identity_setting: string
    task: string
    output: string[]
}

/**
 * @description Handler agent (kind = 2)
 */
export interface HandleAgent extends AgentBase {
    deal: string
}

/**
 * @description Painter agent (kind = 3)
 */
export interface PainterAgent extends AgentBase {
    identity_setting: string
    style: string
}

/**
 * @description 创建 agent 的类型
 */
export type CreateAgentData = AnalyseAgent | JudgeAgent | HandleAgent | PainterAgent

/**
 * @description 更新 agent 的类型
 */
export type UpdateAgentData = { id: string } & CreateAgentData

/**
 * @description 创建agent
 */
export async function createAgent(data: CreateAgentData) {
    const res = await request.post<CreateRes>('/agent/create', data)
    return res.data
}

interface CreateRes {
    code: number
    msg: string
    payload: string
}

/**
 * @description update agent
 */
export async function updateAgent(data: UpdateAgentData) {
    const res = await request.post('/agent/update', data)
    return res
}

/**
 * @description 删除的接口
 */
interface deleteAgent {
    id: string
}

/**
 * @description delete agent
 */
export async function deleteAgent(id: string) {
    const res = await request.get(`/agent/delete?id=${id}`)
    return res
}

/**
 * @description get the list of agents
 */
export async function getAgentList(kind: number): Promise<AgentListRes> {
    const res = await request.get(`/agent/list?kind=${kind}`)
    return res.data
}

/**
 * @description agent list
 */
interface AgentListRes {
    code: number
    msg: string
    payload: Agent[]
}

export type Agent = AnalyseAgent | JudgeAgent | HandleAgent | PainterAgent

/**
 * @description call agent
 */
export async function callAgent(data: CallAgentData) {
    const response = await fetch('http://127.0.0.1:5000/call/one', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!response.body) {
        throw new Error('Response body is empty');
    }

    return response;
}


interface CallAgentData {
    id: string
    kind: number
    input: string
}

interface SceneData {
    [key: string]: any;
}

const apiRequest = async(endpoint: string, data: any)=> {
    try {
        const response = await request.post(endpoint,data);
        return response.data;
    }catch (error) {
        console.error(error);
        throw error;
    }
}

/**
 * @description 创建场景
 */
export const createScene = async(data: SceneData) => {
    return await apiRequest('/scene/create',data);
}

/**
 * @description 更新场景
 */
export const updateScene = async(data: SceneData) => {
    return await apiRequest('/scene/update', data);
}

/**
 * @description 删除场景
 */
export const deleteScene = async(data:SceneData) => {
    return await apiRequest('/scene/delete', data);
}

/**
 * @description 获取场景列表
 */
export const getSceneList = async(data:SceneData) => {
    return await apiRequest('/scene/list', data);
}

/**
 * @description 获取场景详情
 */

export const getSceneDetail = async(data: SceneData) => {
    return await apiRequest('/scene/get', data);
}

export interface Scene {
    id: string
    name: string
    update_time: string
    create_time: string
    agents: Agent[]
}
