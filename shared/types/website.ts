import { GeneratedContent } from './content';
import { IdeaSummary } from './idea';

export interface UserWebsite {
  websiteId: string;
  userId: string;
  subdomain: string;
  ideaSummary: IdeaSummary;
  sections: WebsiteSection[];
  customization: SiteCustomization;
  deploymentStatus: DeploymentStatus;
  createdAt: Date;
  updatedAt: Date;
}

export interface WebsiteSection {
  sectionType: 'marketing' | 'team' | 'funding' | 'research';
  content: GeneratedContent[];
  isActive: boolean;
  order: number;
}

export interface SiteCustomization {
  theme: string;
  primaryColor: string;
  secondaryColor: string;
  logo?: string;
  customCSS?: string;
  navigation: NavigationItem[];
}

export interface NavigationItem {
  label: string;
  path: string;
  isActive: boolean;
  order: number;
}

export type DeploymentStatus = 'pending' | 'building' | 'deployed' | 'failed';

export interface CreateWebsiteRequest {
  ideaId: string;
  subdomain: string;
  customization?: Partial<SiteCustomization>;
}

export interface UpdateWebsiteRequest {
  websiteId: string;
  sections?: WebsiteSection[];
  customization?: Partial<SiteCustomization>;
}