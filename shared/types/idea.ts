export interface IdeaSummary {
  ideaId: string;
  userId: string;
  title: string;
  description: string;
  importance: string;
  targetBeneficiaries: string;
  implementationMethod: string;
  significance: string;
  uniqueness: string;
  additionalDetails: Record<string, string>;
  status: 'draft' | 'complete' | 'implemented';
  createdAt: Date;
  updatedAt: Date;
}

export interface IdeaSession {
  sessionId: string;
  userId: string;
  responses: QuestionResponse[];
  completionStatus: SessionStatus;
  createdAt: Date;
  updatedAt: Date;
}

export interface QuestionResponse {
  questionId: string;
  question: string;
  answer: string;
  followUpPrompts?: string[];
}

export type SessionStatus = 'in_progress' | 'completed' | 'abandoned';

export interface CreateIdeaRequest {
  title: string;
  description: string;
  importance: string;
  targetBeneficiaries: string;
  implementationMethod: string;
  significance: string;
  uniqueness: string;
  additionalDetails?: Record<string, string>;
}

export interface UpdateIdeaRequest extends Partial<CreateIdeaRequest> {
  ideaId: string;
}