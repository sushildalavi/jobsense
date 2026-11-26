import { redirect } from 'next/navigation'
import Link from 'next/link'
import {
  Zap,
  Brain,
  Mail,
  Calendar,
  BarChart3,
  FileText,
  ChevronRight,
  Search,
  Send,
  TrendingUp,
  ArrowRight,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

const features = [
  {
    icon: Search,
    title: 'Intelligent Job Discovery',
    description: 'Pulls listings through Apify actors and scores them against your profile.',
    color: 'text-indigo-400',
    bg: 'bg-indigo-500/10 border-indigo-500/20',
  },
  {
    icon: FileText,
    title: 'Smart Resume Tailoring',
    description: 'Rewrites your resume text to emphasize what a job asks for, for you to review.',
    color: 'text-violet-400',
    bg: 'bg-violet-500/10 border-violet-500/20',
  },
  {
    icon: Mail,
    title: 'Email Intelligence',
    description: 'Classifies recruiting threads from Gmail, such as invites, rejections and assessments.',
    color: 'text-cyan-400',
    bg: 'bg-cyan-500/10 border-cyan-500/20',
  },
  {
    icon: Calendar,
    title: 'Interview Scheduler',
    description: 'Creates calendar events from interview times found in email.',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10 border-emerald-500/20',
  },
  {
    icon: BarChart3,
    title: 'Analytics Dashboard',
    description: 'Track your application funnel, match scores, and response rates with detailed insights.',
    color: 'text-amber-400',
    bg: 'bg-amber-500/10 border-amber-500/20',
  },
]

const steps = [
  {
    num: '01',
    title: 'Upload Your Resume',
    description: 'Upload your master resume. A language model can extract your skills and experience.',
  },
  {
    num: '02',
    title: 'Sync and Score Jobs',
    description: 'Sync listings from your configured sources and rank them by fit score.',
  },
  {
    num: '03',
    title: 'Tailor and Track',
    description: 'Tailor a resume, apply on the employer site, and track every stage to offer.',
  },
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-secondary/5 rounded-full blur-3xl" />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-border bg-background/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <span className="text-lg font-bold text-gradient">JobSense</span>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="ghost" asChild>
              <Link href="/login">Log in</Link>
            </Button>
            <Button asChild>
              <Link href="/register">Get Started</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 pt-24 pb-20 text-center">
        <Badge variant="outline" className="mb-6 border-primary/30 text-primary bg-primary/5">
          <Brain className="w-3 h-3 mr-1.5" />
          Uses OpenAI or Anthropic models
        </Badge>
        <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-6">
          Your{' '}
          <span className="text-gradient">AI-Powered</span>
          <br />
          Job Search Copilot
        </h1>
        <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto mb-10">
          JobSense scores job listings against your profile, drafts tailored resumes, and keeps
          every application in one place.
        </p>
        <div className="flex items-center justify-center gap-4 flex-wrap">
          <Button size="xl" asChild className="shadow-glow">
            <Link href="/register">
              Start for Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
          </Button>
          <Button size="xl" variant="outline" asChild>
            <Link href="/login">Sign In</Link>
          </Button>
        </div>

      </section>

      {/* Features */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Everything you need to land the job</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Tools for each stage of a job search, from listing to offer.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feat) => (
            <div
              key={feat.title}
              className={`rounded-xl border p-6 hover:border-primary/30 transition-all ${feat.bg}`}
            >
              <div className={`w-10 h-10 rounded-lg bg-background flex items-center justify-center mb-4`}>
                <feat.icon className={`w-5 h-5 ${feat.color}`} />
              </div>
              <h3 className="text-lg font-semibold mb-2">{feat.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{feat.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">How JobSense works</h2>
          <p className="text-muted-foreground">Three steps</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, i) => (
            <div key={step.num} className="relative text-center">
              {i < steps.length - 1 && (
                <div className="hidden md:block absolute top-8 left-[60%] w-[80%] h-px bg-gradient-to-r from-primary/50 to-transparent" />
              )}
              <div className="w-16 h-16 rounded-2xl bg-gradient-primary flex items-center justify-center mx-auto mb-6 shadow-glow">
                <span className="text-xl font-black text-white">{step.num}</span>
              </div>
              <h3 className="text-xl font-semibold mb-3">{step.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{step.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-20">
        <div className="rounded-2xl border border-primary/20 bg-gradient-to-br from-primary/10 to-secondary/10 p-12 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Organize your job search
          </h2>
          <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
            Create an account to start tracking your applications.
          </p>
          <Button size="xl" asChild className="shadow-glow">
            <Link href="/register">
              Get Started Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-border py-8">
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-md bg-gradient-primary flex items-center justify-center">
              <Zap className="w-3 h-3 text-white" />
            </div>
            <span className="text-sm font-semibold text-gradient">JobSense</span>
          </div>
          <p className="text-xs text-muted-foreground">
            &copy; {new Date().getFullYear()} JobSense. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}
