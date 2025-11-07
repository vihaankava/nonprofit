import { IdeaSummary } from './idea';

export interface ContentRequest {
  type: 'marketing' | 'team' | 'funding' | 'research';
  subtype: string; // 'flyer', 'email', 'pitch', etc.
  ideaContext: IdeaSummary;
  additionalParams?: Record<string, any>;
}

export interface GeneratedContent {
  contentId: string;
  type: string;
  subtype: string;
  content: string;
  metadata: ContentMetadata;
  generatedAt: Date;
}

export interface ContentMetadata {
  wordCount?: number;
  language?: string;
  tone?: string;
  targetAudience?: string;
  generationModel?: string;
  version?: number;
}

export interface ContentLibrary {
  userId: string;
  marketingContent: GeneratedContent[];
  teamContent: GeneratedContent[];
  fundingContent: GeneratedContent[];
  researchContent: GeneratedContent[];
  lastUpdated: Date;
}

export interface CreateContentRequest {
  type: ContentRequest['type'];
  subtype: string;
  ideaId: string;
  additionalParams?: Record<string, any>;
}

export interface ContentGenerationResponse {
  success: boolean;
  content?: GeneratedContent;
  error?: string;
}